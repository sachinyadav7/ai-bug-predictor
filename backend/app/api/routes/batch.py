from fastapi import APIRouter, UploadFile, File
from typing import List
from app.api.routes.predict import predict, PredictRequest

router = APIRouter()

def detect_language(filename: str) -> str:
    ext = filename.split('.')[-1].lower()
    mapping = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'go': 'go',
        'rb': 'ruby',
        'php': 'php'
    }
    return mapping.get(ext, 'python')

@router.post("/batch-scan")
async def batch_scan(files: List[UploadFile]):
    """
    Scan multiple files
    """
    results = []
    
    for file in files:
        content = await file.read()
        try:
            code = content.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Skipping binary or encoding error file: {file.filename}")
            continue
        
        # Detect language from extension
        language = detect_language(file.filename)
        
        request = PredictRequest(
            code=code,
            language=language,
            filename=file.filename
        )
        
        try:
            # We call the predict function logic directly if possible, or refactor.
            # Since predict is an async route handler, calling it directly works if structure aligns.
            # But predict expects a Request object if accessed via route.
            # However, I defined `predict` as a function accepting `PredictRequest`.
            # So I can call it directly!
            result = await predict(request)
            results.append({
                'filename': file.filename,
                'analysis': result
            })
        except Exception as e:
            results.append({
                'filename': file.filename,
                'error': str(e)
            })
    
    return {'files': results}
