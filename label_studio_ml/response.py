from typing import Dict, Optional, List, Any, Union

from label_studio_sdk.label_interface.region import Region
from pydantic import BaseModel


def serialize_regions(result):
    """ """
    res = []
    relations = []
    for r in result:
        if isinstance(r, Region):
            res.append(r._dict())
            if r.has_relations:
                relations.append(r._dict_relations())
        else:
            res.append(r)

    return res + relations


class PredictionValue(BaseModel):
    """ """

    model_version: Optional[Any] = None
    score: Optional[float] = 0.00
    result: Optional[List[Union[Dict[str, Any], Region]]]

    # cluster: Optional[Any] = None
    # neighbors: Optional[Any] = None

    class Config:
        allow_population_by_field_name = True

    def serialize(self):
        """ """
        return {
            "model_version": self.model_version,
            "score": self.score,
            "result": serialize_regions(self.result),
        }


class ModelResponse(BaseModel):
    """
    """
    model_version: Optional[str] = None
    predictions: List[PredictionValue]

    def has_model_version(self) -> bool:
        return bool(self.model_version)

    def update_predictions_version(self) -> None:
        """
        """
        for prediction in self.predictions:
            if not prediction.model_version:
                prediction.model_version = self.model_version

    def set_version(self, version: str) -> None:
        """
        """
        self.model_version = version
        # Set the version for each prediction
        self.update_predictions_version()

    def serialize(self):
        """
        """
        return {
            "model_version": self.model_version,
            "predictions": [p.serialize() for p in self.predictions]
        }
