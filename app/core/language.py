from __future__ import annotations
from typing import List, Dict
from pydantic import BaseModel
from .models import LanguageId

class LanguageMode(BaseModel):
    id:LanguageId
    extentions:List[str]
    comment_line:str

LANGUAGES: Dict[LanguageId,LanguageMode] = {
    "python" : LanguageMode(
        id="python",
        extensions=[".py"],
        comment_line="#"
    ),

    "javascript":LanguageMode(
        id="javascript",
        extensions=[".js",".mjs",".cjs"],
        comment_line="//"
    ),
    
    "cpp": LanguageMode(
        id="cpp",
        extensions=[".cpp", ".cc", ".hpp", ".h"],
        comment_line="//"
    ),
        "plaintext": LanguageMode(
        id="plaintext",
        extensions=[],
        comment_line="//"
    ),
}

def detect_language(file_name:str)->LanguageId:
    file_name = file_name.lower()
    for lang in LANGUAGES.values():
        for ext in lang.extentions:
            if file_name.endswith(ext):
                return lang.id
            
    return "plaintext"