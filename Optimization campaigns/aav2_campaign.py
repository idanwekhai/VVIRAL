
import json
import tqdm as notebook_tqdm
import pandas as pd
import numpy as np

from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process.kernels import *
from baybe.searchspace import SearchSpace
from baybe.targets import NumericalTarget
from baybe.objectives import SingleTargetObjective
from baybe.searchspace import SearchSpace

from baybe.parameters import (
    CategoricalParameter,
    NumericalDiscreteParameter,
    NumericalContinuousParameter,
)

from baybe.recommenders import (
    SequentialGreedyRecommender,
    TwoPhaseMetaRecommender,
    RandomRecommender
)
from baybe.acquisition.acqfs import qExpectedImprovement
from baybe import Campaign
from surrogate_model import gp_model


target = NumericalTarget(
    name="Total Capsids",
    mode="MAX",
)
objective = SingleTargetObjective(target=target)


parameters = [
    NumericalDiscreteParameter(
        name="Pure",
        values=[0, 1],
    ),
    NumericalDiscreteParameter(
        name="Elution pH",
        # bounds=(5, 9),
        values = list(np.arange(5, 9.5, 0.5))
    ),
    NumericalDiscreteParameter(
        name="Wash pH",
        # bounds=(5, 9),
        values = list(np.arange(5, 9.5, 0.5))
    ),
    NumericalDiscreteParameter(
        name="Equilibration pH",
        values=[7.0, 0],
    ),
    NumericalContinuousParameter(
        name="Elution Conductivity",
        bounds=(10, 101),
        # values = np.arange(10, 101, 1)
    ),
    NumericalDiscreteParameter(
        name="Wash Conductivity",
        # bounds=(1, 16),
        values = np.arange(1, 16, 1)
    ),
    NumericalDiscreteParameter(
        name="Equilibration Conductivity",
        values=[2.5, 0],
    ),
    NumericalDiscreteParameter(
        name="System Flowrate Elution (cm/h)",
        values=[306, 0],
    ),
    NumericalContinuousParameter(
        name="Sample Flowrate Elution (cm/h)",
        bounds=(130, 601),
        # values = np.arange(10, 101, 1)
    ),
    NumericalDiscreteParameter(
        name="Sample Volume",
        values=[5, 10, 15, 20, 25, 30],
    ),
    CategoricalParameter(
        name="serotype",
        values=['AAV10','AAV2'],
        encoding="OHE",  # one-hot encoding of categories
    ),
    CategoricalParameter(
        name="from",
        values=['LFT', 'ELU'],
        encoding="OHE",  # one-hot encoding of categories
    ),
    CategoricalParameter(
        name="resin",
        values=['AAVA2', 'AAVA3'],
        encoding="OHE",  # one-hot encoding of categories
    )

]


searchspace = SearchSpace.from_product(parameters)

# find indices of parameter values that you dont want recommended
dont_recommend_idxs_1 = searchspace.discrete.exp_rep['serotype'] != 'AAV2'
# restrict recommendations via metadata
searchspace.discrete.metadata.loc[dont_recommend_idxs_1, 'dont_recommend'] = True

dont_recommend_idxs_2 = searchspace.discrete.exp_rep['from'] != 'ELU'
searchspace.discrete.metadata.loc[dont_recommend_idxs_2, 'dont_recommend'] = True

dont_recommend_idxs_3 = searchspace.discrete.exp_rep['resin'] != 'AAVA3'
searchspace.discrete.metadata.loc[dont_recommend_idxs_3, 'dont_recommend'] = True

dont_recommend_idxs_4 = searchspace.discrete.exp_rep['Pure'] != 0
searchspace.discrete.metadata.loc[dont_recommend_idxs_4, 'dont_recommend'] = True

dont_recommend_idxs_5 = searchspace.discrete.exp_rep['Equilibration pH'] != 7.0
searchspace.discrete.metadata.loc[dont_recommend_idxs_5, 'dont_recommend'] = True

dont_recommend_idxs_6 = searchspace.discrete.exp_rep['Equilibration Conductivity'] != 2.5
searchspace.discrete.metadata.loc[dont_recommend_idxs_6, 'dont_recommend'] = True

dont_recommend_idxs_7 = searchspace.discrete.exp_rep['System Flowrate Elution (cm/h)'] != 306
searchspace.discrete.metadata.loc[dont_recommend_idxs_7, 'dont_recommend'] = True

gp_surrogate = gp_model()
recommender = TwoPhaseMetaRecommender(
    initial_recommender=RandomRecommender(),
recommender=SequentialGreedyRecommender(acquisition_function=qExpectedImprovement(), surrogate_model=gp_surrogate)
)

campaign = Campaign(searchspace, objective, recommender)
df = campaign.recommend(batch_size=15)


# Other Utils

# campaign_json = campaign.to_json()
# with open('AAV2_AAVA3_campaign.json', 'w', encoding='utf-8') as f:
#     json.dump(campaign_json, f, ensure_ascii=False, indent=4)

# new_add = pd.read_csv("process_filecsv")
# new_add["Total Capsids"] = log_transform(new_add["Total Capsids"])
# campaign.add_measurements(new_add, numerical_measurements_must_be_within_tolerance = False)