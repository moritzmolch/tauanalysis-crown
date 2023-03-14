from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List, Union
import os
from .producers import event as event
from .producers import genparticles as genparticles
from .producers import jets as jets
from .producers import met as met
from .producers import muons as muons
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import scalefactors as scalefactors
from .producers import taus as taus
from .producers import triggers as triggers
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q

# from code_generation.configuration import Configuration
from code_generation.friend_trees import FriendTreeConfiguration


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
):
    if quantities_map is None:
        quantities_map = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dyjets_shift_quantities_map.json",
        )
    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    configuration.add_config_parameters(
        ["mt", "et"],
        {
            "muon_sf_file": "data/embedding/muon_2018UL.json.gz",
            "muon_id_sf": "ID_pt_eta_bins",
            "muon_iso_sf": "Iso_pt_eta_bins",
        },
    )

    configuration.add_producers(
        ["mt", "et"],
        [
            scalefactors.MuonIDSF_friends_1,
            scalefactors.MuonIsoSF_friends_1,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.id_wgt_mu_friend_1,
            q.iso_wgt_mu_friend_1,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
