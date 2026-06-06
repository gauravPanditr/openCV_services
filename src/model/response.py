from pydantic import BaseModel

class ImageAnalysisResponse(BaseModel):
    claim_id: str
    ela_score: float
    edited_suspected: bool

    is_duplicate: bool
    duplicate_of: str | None = None
    similarity_score: float | None = None
    damage_confidence: float | None = None
    
    

    damage_level: str
    