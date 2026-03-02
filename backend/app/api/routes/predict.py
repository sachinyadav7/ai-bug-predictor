from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.core.model import model_manager
from app.core.preprocessor import CodePreprocessor
import time

router = APIRouter()

class PredictRequest(BaseModel):
    code: str
    language: str = "python"
    filename: Optional[str] = None
    include_explanation: bool = False

class FunctionResult(BaseModel):
    function_name: str
    line_start: int
    line_end: int
    is_buggy: bool
    confidence: float
    risk_level: str
    highlighted_tokens: Optional[List[dict]] = None

class PredictResponse(BaseModel):
    file_risk_score: float
    functions_analyzed: int
    buggy_functions_count: int
    results: List[FunctionResult]
    processing_time_ms: float
    language: str

@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Analyze code and predict bug probability
    """
    start_time = time.time()
    
    try:
        # Preprocess
        preprocessor = CodePreprocessor(request.language)
        functions = preprocessor.extract_functions(request.code)
        
        if not functions:
            raise HTTPException(status_code=400, detail="No functions found in code")
        
        # Predict for each function
        results = []
        buggy_count = 0
        total_confidence = 0
        
        for func in functions:
            prediction = model_manager.predict(func['code'])
            
            if prediction['is_buggy']:
                buggy_count += 1
            
            total_confidence += prediction['confidence']
            
            result = FunctionResult(
                function_name=func['name'],
                line_start=func.get('start_line', 0),
                line_end=func.get('end_line', 0),
                is_buggy=prediction['is_buggy'],
                confidence=prediction['confidence'],
                risk_level=prediction['risk_level']
            )
            
            # Add explanation if requested
            if request.include_explanation:
                # Placeholder for explanation logic
                pass 
            
            results.append(result)
        
        # Calculate file-level risk
        file_risk = total_confidence / len(functions) if functions else 0
        
        processing_time = (time.time() - start_time) * 1000
        
        # Record stats
        try:
            from app.core.stats import stats_manager
            stats_manager.record_scan(buggy_count, processing_time)
        except Exception as stats_error:
            print(f"Failed to record stats: {stats_error}")
        
        return PredictResponse(
            file_risk_score=file_risk,
            functions_analyzed=len(functions),
            buggy_functions_count=buggy_count,
            results=results,
            processing_time_ms=processing_time,
            language=request.language
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
