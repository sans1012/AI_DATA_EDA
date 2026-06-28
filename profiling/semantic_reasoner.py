from core.semantic_metadata import SemanticMetadata
from utils.logger import get_logger

log = get_logger(__name__)


class SemanticReasoner:

    def __init__(self):

        self.metric_keywords = [

            "sales",
            "profit",
            "revenue",
            "income",
            "amount",
            "price",
            "cost",
            "salary",
            "fare",
            "charges",
            "balance",
            "quantity",
            "qty",
            "score",
            "rating",
            "weight",
            "height",
            "age",
            "tenure"

        ]

        self.target_keywords = [

            "target",
            "label",
            "class",
            "status",
            "outcome",
            "default",
            "fraud",
            "churn",
            "survived"

        ]

        self.identifier_keywords = [

            "id",
            "uuid",
            "invoice",
            "transaction",
            "customerid",
            "userid",
            "orderid"

        ]

        self.datetime_keywords = [

            "date",
            "time",
            "timestamp",
            "year",
            "month",
            "day"

        ]

        self.geo_keywords = [

            "country",
            "city",
            "state",
            "region",
            "zip",
            "postal"

        ]

    def reason(self, columns_metadata):

        log.info("Running Semantic Reasoner...")

        semantic_results = []

        for column in columns_metadata:

            name = column.name.lower()

            semantic = SemanticMetadata(

                column=column.name,

                dtype=column.dtype,

                unique_count=column.unique_count,

                unique_ratio=column.unique_ratio,

                missing_pct=column.missing_pct,

                sample_values=column.sample_values

            )

            score = {

                "Identifier": 0,

                "Metric": 0,

                "Dimension": 0,

                "Target": 0,

                "Datetime": 0,

                "Geography": 0,

                "Text": 0

            }

            notes = []

            # -----------------------------------------
            # Identifier
            # -----------------------------------------

            if any(k in name for k in self.identifier_keywords):

                score["Identifier"] += 90

                notes.append("Column name indicates identifier.")

            if column.unique_ratio > 0.98:

                score["Identifier"] += 50

                notes.append("Almost every value is unique.")

            # -----------------------------------------
            # Datetime
            # -----------------------------------------

            if column.is_datetime:

                score["Datetime"] += 100

                notes.append("Detected datetime column.")

            elif any(k in name for k in self.datetime_keywords):

                score["Datetime"] += 70

            # -----------------------------------------
            # Geography
            # -----------------------------------------

            if any(k in name for k in self.geo_keywords):

                score["Geography"] += 80

                notes.append("Looks like geographical information.")

            # -----------------------------------------
            # Target
            # -----------------------------------------

            if any(k in name for k in self.target_keywords):

                score["Target"] += 90

                notes.append("Column name suggests prediction target.")

            elif column.is_binary:

                score["Target"] += 40

                notes.append("Binary feature.")

            # -----------------------------------------
            # Metric
            # -----------------------------------------

            if column.is_numeric:

                score["Metric"] += 50

                notes.append("Numeric column.")

                if column.statistics:

                    if column.statistics.get("std", 0) > 0:

                        score["Metric"] += 20

            if any(k in name for k in self.metric_keywords):

                score["Metric"] += 50

            # -----------------------------------------
            # Text
            # -----------------------------------------

            if column.is_categorical:

                if column.unique_ratio > 0.80:

                    score["Text"] += 60

                    semantic.is_high_cardinality = True

                    notes.append("High-cardinality categorical column.")

            # -----------------------------------------
            # Default Dimension
            # -----------------------------------------

            score["Dimension"] += 20

            # -----------------------------------------
            # Final Role
            # -----------------------------------------

            role = max(score, key=score.get)

            confidence = min(round(score[role] / 100, 2), 1.0)

            semantic.role = role
            semantic.semantic_type = role.lower()
            semantic.confidence = confidence

            semantic.is_metric = role == "Metric"
            semantic.is_dimension = role == "Dimension"
            semantic.is_identifier = role == "Identifier"
            semantic.is_target = role == "Target"
            semantic.is_datetime = role == "Datetime"
            semantic.is_geography = role == "Geography"
            semantic.is_text = role == "Text"
            semantic.is_binary = column.is_binary

            # -----------------------------------------
            # Recommended Chart
            # -----------------------------------------

            if semantic.is_metric:

                if column.unique_count <= 10:

                    semantic.recommended_chart = "bar"

                else:

                    semantic.recommended_chart = "histogram"

            elif semantic.is_dimension:

                semantic.recommended_chart = "bar"

            elif semantic.is_geography:

                semantic.recommended_chart = "bar"

            elif semantic.is_target:

                semantic.recommended_chart = "count"

            # -----------------------------------------
            # Statistical Tests
            # -----------------------------------------

            if semantic.is_metric:

                semantic.statistical_tests.extend(

                    [

                        "Pearson",

                        "Spearman"

                    ]

                )

            elif semantic.is_dimension:

                semantic.statistical_tests.extend(

                    [

                        "Chi Square",

                        "Cramers V"

                    ]

                )

            elif semantic.is_target:

                semantic.statistical_tests.append(

                    "ANOVA"

                )

            semantic.notes = notes

            semantic_results.append(semantic)

        log.info("Semantic Reasoning Complete.")

        return semantic_results