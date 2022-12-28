import os
import re
import bs4
import more_itertools
import requests
from flatten_everything import ProtectedTuple, flatten_everything
from a_pandas_ex_enumerate_groups import pd_add_enumerate_group

pd_add_enumerate_group()
import pandas as pd


def html_to_css_selector(htmlstring, parser="html.parser"):
    if os.path.exists(htmlstring):
        with open(htmlstring, mode="rb") as f:
            htmlstring = f.read()
    elif re.search(r"^https?://", str(htmlstring), flags=re.I) is not None:
        htmlstring = requests.get(htmlstring).content
    soup = bs4.BeautifulSoup(htmlstring, parser)
    allcss = []
    for tag in soup.findAll(True):
        alltag = tag.name
        attsep = []
        for key, item in tag.attrs.items():
            if isinstance(item, list):
                item = " ".join(item)
            attr = rf"""[{key}="{item}"]"""
            attsep.append(attr)
            alltag += attr
        allcss.append((alltag, tag, tag.attrs.items(), tag.name, attsep))
    return allcss


def get_dataframe_css(html, parser="html.parser", ignore_tags=("html", "body")):
    fe = html_to_css_selector(html, parser=parser)
    wholeall = []
    for fee in fe:
        allres = str(fee[1])
        subbi = []
        for part in more_itertools.powerset(fee[-1]):
            if fee[-2].lower() in ignore_tags:
                continue
            vra = fee[-2] + ("".join(list(part)))
            if not "[" in vra:
                continue
            subbi.append(ProtectedTuple((allres, vra)))
        wholeall.append(subbi.copy())
    df = pd.DataFrame(flatten_everything(wholeall)).rename(
        columns={0: "html", 1: "selector"}
    )
    df = df.d_enumerate_all_groups_in_all_columns(prefix="group_")
    return df


def pd_add_css_selector_from_html():
    pd.Q_selector_from_html = get_dataframe_css


