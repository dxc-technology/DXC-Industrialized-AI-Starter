"""
Importing all functions into ai namespace
"""

from .AI_guild.AI_guild import guild_member_should_apply_for_badge
from .AI_guild.AI_guild import apply_for_an_ai_badge
from .AI_guild.AI_guild import AI_Guild_Role
from .AI_guild.AI_guild import AI_Badge

from .read_data.read_json import flatten_json_into_dataframe
from .read_data.read_json import get_file_path_json
from .read_data.read_json import read_data_frame_from_remote_json
from .read_data.read_json import read_data_frame_from_local_json
from .read_data.read_json import read_data_frame_from_local_json
from .read_data.read_excel import get_file_path_excel
from .read_data.read_excel import read_data_frame_from_local_excel_file
from .read_data.read_csv import get_file_path_csv
from .read_data.read_csv import read_data_frame_from_local_csv
from .read_data.read_csv import read_data_frame_from_remote_csv
from .read_data.read_json import read_data_frame_from_remote_json

from .clean_data.clean_data import clean_dataframe

from .visualization.visualization import explore_features
from .visualization.visualization import visualize_missing_data
from .visualization.visualization import plot_distributions
from .visualization.visualization import explore_complete_data

from .pipeline.pipeline import convert_dates_from_arrow_to_string
from .pipeline.pipeline import write_raw_data
from .pipeline.pipeline import access_data_from_pipeline
from .pipeline.pipeline import store_data_from_pipeline

from .run_model.run_model import get_data_from_pipeline
from .run_model.run_model import run_experiment
from .run_model.run_model import model
from .run_model.run_model import prediction
from .run_model.run_model import regression
from .run_model.run_model import classification
from .run_model.run_model import tpot_regression
from .run_model.run_model import tpot_classification
from .run_model.interpret_model import Global_Model_Explanation
from .run_model.interpret_model import Explanation_Dashboard
# from .run_model.clustering import Clustering
# from .sentiment_analysis.sentiment_analysis import texts_from_df
# from .sentiment_analysis.sentiment_analysis import get_model_learner
# from .sentiment_analysis.sentiment_analysis import get_predictor
# from .unsupervised_sentiment_analysis.kmeans_sentiment_analysis import get_text_clean
# from .unsupervised_sentiment_analysis.kmeans_sentiment_analysis import kmeans_sentiment_analyzer
# from .unsupervised_sentiment_analysis.kmeans_sentiment_analysis import kmeans_sentiment_predictor

from .publish_microservice.publish_microservice import publish_microservice

from .deploy_app.build_app import generate_req_files
from .deploy_app.build_app import generate_app_script
from .deploy_app.build_app import publish_model

# from .deep_learning.image_classifier import create_training_data
# from .deep_learning.image_classifier import seggregate_data
# from .deep_learning.image_classifier import split_normalize_data
# from .deep_learning.image_classifier import image_classifier

from .logging.pipeline_logging          import pipeline_log
from .logging.experiment_design_logging import experiment_design_log
from .logging.microservice_logging      import microservice_design_log

from .datasets._base import load_data
# from .datasets._base import load_data_details
# from .datasets._base import get_data

