"""File management API"""
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.file import File as FileModel
from app.models.user import User as UserModel
from app.core.security import get_current_user


# 文件存储目录
UPLOAD_DIR = Path("data/files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    "image": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"},
    "document": {".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx"},
    "archive": {".zip", ".rar", ".7z", ".tar", ".gz"}
}

# 最大文件大小 (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024


router = APIRouter()


def get_file_category(filename: str) -> str:
    """根据文件扩展名获取文件类别"""
    ext = Path(filename).suffix.lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    return "other"


def validate_file(filename: str, file_size: int) -> tuple[bool, Optional[str]]:
    """验证文件"""
    ext = Path(filename).suffix.lower()

    # 检查文件大小
    if file_size > MAX_FILE_SIZE:
        return False, f"文件大小超过限制（最大 {MAX_FILE_SIZE // (1024 * 1024)}MB）"

    # 检查文件扩展名
    all_extensions = set()
    for extensions in ALLOWED_EXTENSIONS.values():
        all_extensions.update(extensions)

    if ext not in all_extensions:
        return False, f"不支持的文件类型: {ext}"

    return True, None


def format_file_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


@router.post("/upload")
def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传文件"""
    try:
        # 读取文件内容
        content = file.file.read()
        file_size = len(content)

        # 验证文件
        is_valid, error_msg = validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # 生成唯一文件名
        ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{ext}"

        # 创建用户目录和日期目录
        user_dir = UPLOAD_DIR / str(current_user.id)
        date_dir = user_dir / datetime.now().strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)

        # 保存文件
        file_path = date_dir / unique_filename
        with open(file_path, "wb") as f:
            f.write(content)

        # 获取文件类别和 MIME 类型
        category = get_file_category(file.filename)
        mime_type = file.content_type or "application/octet-stream"

        # 保存文件信息到数据库
        db_file = FileModel(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            mime_type=mime_type,
            uploaded_by=current_user.id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return {
            "id": db_file.id,
            "filename": db_file.original_filename,
            "file_size": db_file.file_size,
            "file_size_formatted": format_file_size(db_file.file_size),
            "category": category,
            "mime_type": db_file.mime_type,
            "uploaded_at": db_file.uploaded_at.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.get("/", response_model=List[dict])
def list_files(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    try:
        query = db.query(FileModel).filter(FileModel.uploaded_by == current_user.id)

        # 按类别过滤
        if category:
            category_extensions = ALLOWED_EXTENSIONS.get(category, set())
            if category_extensions:
                # 先获取所有文件
                files = query.all()
                # 筛选符合扩展名的文件
                filtered_files = [
                    file for file in files
                    if Path(file.original_filename).suffix.lower() in category_extensions
                ]
                # 排序和分页
                filtered_files.sort(key=lambda x: x.uploaded_at, reverse=True)
                return [file.to_dict() for file in filtered_files[skip:skip+limit]]

        # 默认查询
        files = query.order_by(FileModel.uploaded_at.desc()).offset(skip).limit(limit).all()
        return [file.to_dict() for file in files]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")


@router.get("/{file_id}")
def get_file_info(
    file_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件信息"""
    try:
        file = db.query(FileModel).filter(
            FileModel.id == file_id,
            FileModel.uploaded_by == current_user.id
        ).first()

        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")

        file_info = file.to_dict()
        file_info["file_size_formatted"] = format_file_size(file.file_size)
        file_info["category"] = get_file_category(file.original_filename)

        return file_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件信息失败: {str(e)}")


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载文件"""
    try:
        file = db.query(FileModel).filter(
            FileModel.id == file_id,
            FileModel.uploaded_by == current_user.id
        ).first()

        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")

        # 检查文件是否存在
        if not os.path.exists(file.file_path):
            raise HTTPException(status_code=404, detail="文件已被删除")

        return FileResponse(
            path=file.file_path,
            filename=file.original_filename,
            media_type=file.mime_type
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件下载失败: {str(e)}")


@router.get("/{file_id}/preview")
def preview_file(
    file_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """预览文件（仅支持图片）"""
    try:
        file = db.query(FileModel).filter(
            FileModel.id == file_id,
            FileModel.uploaded_by == current_user.id
        ).first()

        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")

        # 检查是否为图片
        category = get_file_category(file.original_filename)
        if category != "image":
            raise HTTPException(status_code=400, detail="该文件类型不支持预览")

        # 检查文件是否存在
        if not os.path.exists(file.file_path):
            raise HTTPException(status_code=404, detail="文件已被删除")

        return FileResponse(
            path=file.file_path,
            media_type=file.mime_type
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件预览失败: {str(e)}")


@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文件"""
    try:
        file = db.query(FileModel).filter(
            FileModel.id == file_id,
            FileModel.uploaded_by == current_user.id
        ).first()

        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")

        # 删除物理文件
        if os.path.exists(file.file_path):
            os.remove(file.file_path)

        # 删除数据库记录
        db.delete(file)
        db.commit()

        return {"message": "文件删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")


@router.get("/stats/summary")
def get_file_stats(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件统计信息"""
    try:
        # 获取所有文件
        files = db.query(FileModel).filter(FileModel.uploaded_by == current_user.id).all()

        # 统计信息
        total_count = len(files)
        total_size = sum(file.file_size for file in files)

        # 按类别统计
        category_stats = {}
        for file in files:
            category = get_file_category(file.original_filename)
            if category not in category_stats:
                category_stats[category] = {"count": 0, "size": 0}
            category_stats[category]["count"] += 1
            category_stats[category]["size"] += file.file_size

        # 格式化统计信息
        formatted_stats = {
            "total_count": total_count,
            "total_size": total_size,
            "total_size_formatted": format_file_size(total_size),
            "categories": {}
        }

        for category, stats in category_stats.items():
            formatted_stats["categories"][category] = {
                "count": stats["count"],
                "size": stats["size"],
                "size_formatted": format_file_size(stats["size"])
            }

        return formatted_stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")
