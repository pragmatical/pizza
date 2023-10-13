# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(
    BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]
):
    """
    Post-processor component for minifying json (removing whitespace and newlines)

    Component Args:
        (None)

    Fields used:
        - data_model.model_output.completions: the list of completions

    Fields updated:
        - data_model.model_output.completions: the list of completions with json values minified.
            If it fails to parse the json, the original string is used
    """

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        completions = data_model.model_output.completions
        formatted = []

        for c in completions:
            try:
                completion = json.loads(c)
                formatted.append(json.dumps(completion))
            except json.JSONDecodeError:
                formatted.append(c)

        data_model.model_output.completions = formatted

        return data_model
