import os
import uuid
from pathlib import Path
from fastapi import UploadFile
import aiofiles
import blake3


class TempFileHelper:

    def __init__(self, storage_path: str = "uploads", chunk_size: int = 1024 * 1024):
        self.chunk_size = chunk_size
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    async def save_temp(self, file: UploadFile):
        """
        Temporarily save uploaded file + calculate hash in the same write cycle. 
        Return metadata: save name, size (if any), path, hash.
        """
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        dest_path = self.storage_path / unique_name

        hasher = blake3.blake3()

        try:
            await file.seek(0)
            async with aiofiles.open(dest_path, "wb") as out_f:
                while True:
                    chunk = await file.read(self.chunk_size)
                    if not chunk:
                        break
                    await out_f.write(chunk)
                    hasher.update(chunk)

            hexdigest = hasher.hexdigest()
            await file.close()

            return {
                "file_name": unique_name,
                "file_size": file.size,
                "dest_path": str(dest_path),
                "hexdigest": hexdigest,
            }

        except Exception as exc:
            try:
                if dest_path.exists():
                    dest_path.unlink()
            except Exception as e2:
                # log warning.
                pass
            await file.close()
            raise

    def delete_temp(self, file_path: str) -> bool:
        """
        Delete temporary files.
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
        except Exception as e:
            # log hoặc xử lý lỗi nếu cần
            return False
        return False
