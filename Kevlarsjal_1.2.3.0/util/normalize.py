import logging
import pandas as pd
import numpy as np

logger = logging.getLogger('main.normalize')


def normalize_tsxci(data):
    data['Symbol'] = data['Symbol'].str.replace(".","-")
    #Bausch Health Companies Inc. (formerly Valeant Pharmaceuticals) to new ticker code VRX -> BHC
    data['Symbol'] = data['Symbol'].str.replace("VRX","BHC")
    data['Company'] = data['Company'].str.replace("Valeant Pharmaceuticals International Inc.","Bausch Health Companies Inc.")
    return data
