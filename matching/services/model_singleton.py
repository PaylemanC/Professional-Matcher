"""
Singleton para gestión de modelos de ML y cache de embeddings
*Generado automático. 
"""
import hashlib
from typing import Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import numpy as np

class ModelSingleton:
    """Singleton para gestión de modelos de ML"""
    _instance = None
    _models = {}
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._models = {}
            self._initialized = True
    
    def get_sentence_transformer(self, model_name: str = 'all-MiniLM-L6-v2') -> SentenceTransformer:
        if model_name not in self._models:
            self._models[model_name] = SentenceTransformer(model_name)
        return self._models[model_name]
    
    def get_keybert_model(self, model_name: str = 'all-MiniLM-L6-v2') -> KeyBERT:
        keybert_key = f"keybert_{model_name}"
        if keybert_key not in self._models:
            sentence_model = self.get_sentence_transformer(model_name)
            self._models[keybert_key] = KeyBERT(model=sentence_model)
        return self._models[keybert_key]
    
    def clear_models(self):
        self._models.clear()

class EmbeddingCache:
    _cache: Dict[str, np.ndarray] = {}
    _max_size = 1000  
    
    @classmethod
    def _get_hash(cls, text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @classmethod
    def get(cls, text: str) -> Optional[np.ndarray]:
        text_hash = cls._get_hash(text)
        return cls._cache.get(text_hash)
    
    @classmethod
    def set(cls, text: str, embedding: np.ndarray):
        if len(cls._cache) >= cls._max_size:
            oldest_key = next(iter(cls._cache))
            del cls._cache[oldest_key]
        
        text_hash = cls._get_hash(text)
        cls._cache[text_hash] = embedding
    
    @classmethod
    def get_or_compute(cls, text: str, model: SentenceTransformer) -> np.ndarray:
        cached_embedding = cls.get(text)
        if cached_embedding is not None:
            return cached_embedding
        
        embedding = model.encode([text])[0]
        cls.set(text, embedding)
        return embedding
    
    @classmethod
    def get_or_compute_batch(cls, texts: list, model: SentenceTransformer) -> np.ndarray:
        if not texts:
            return np.array([])
            
        embeddings = []
        texts_to_compute = []
        indices_to_compute = []
        
        for i, text in enumerate(texts):
            cached_embedding = cls.get(text)
            if cached_embedding is not None:
                embeddings.append(cached_embedding)
            else:
                embeddings.append(None)
                texts_to_compute.append(text)
                indices_to_compute.append(i)
        
        if texts_to_compute:
            new_embeddings = model.encode(texts_to_compute)
            for i, embedding in enumerate(new_embeddings):
                original_index = indices_to_compute[i]
                text = texts_to_compute[i]
                cls.set(text, embedding)
                embeddings[original_index] = embedding
        
        return np.array(embeddings)
    
    @classmethod
    def clear(cls):
        cls._cache.clear()
    
    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        return {
            'size': len(cls._cache),
            'max_size': cls._max_size,
            'usage_percent': (len(cls._cache) / cls._max_size) * 100
        }

# GLOBAL INSTANCE
model_singleton = ModelSingleton()
