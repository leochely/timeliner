from django.shortcuts import render
from django.template.defaultfilters import date as _date

import six
import numpy as np
import locale
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from .forms import SearchForm
from .models import *

import matplotlib
matplotlib.use('Agg')
# locale.setlocale(locale.LC_ALL, 'fr')

# Create your views here.


def index(request):
    names = []
    dates = []
    graphics = []
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            personnages = Personnage.objects.filter(
                id__in=form.cleaned_data['personnages'])

            events = Evenement.objects.all()
            if form.cleaned_data['categories']:
                for categorie in form.cleaned_data['categories']:
                    events = events.filter(categorie=categorie)

            if not form.cleaned_data["personnages"]:
                title = "Événements de " + \
                    _date(form.cleaned_data['date_depart'], "d M Y") + \
                    " à " + _date(form.cleaned_data['date_fin'], "d M Y")
                events = events.filter(date__range=(
                    form.cleaned_data['date_depart'], form.cleaned_data['date_fin']))
                for event in events:
                    names.append(event.name)
                    dates.append(event.date)
                    if form.cleaned_data["flashback"] and event.flashback_date:
                        names.append(event.name + " flashback")
                        dates.append(event.flashback_date)

                graphics.append(makeGraph(names, dates, title))

            elif form.cleaned_data['combined']:
                title = "Événements pour"
                for personnage in personnages:
                    title += " " + personnage.name + years_between(
                        personnage, form.cleaned_data['date_depart'], form.cleaned_data['date_fin']) + ","
                title = title[:-1]
                title += " de " + _date(form.cleaned_data['date_depart'], "d M Y") + " à " + _date(
                    form.cleaned_data['date_fin'], "d M Y")

                for personnage in personnages:
                    events = events.filter(personnages=personnage)

                for event in events:
                    names.append(event.name)
                    dates.append(event.date)
                    if form.cleaned_data["flashback"] and event.flashback_date:
                        names.append(event.name + " flashback")
                        dates.append(event.flashback_date)

                graphics.append(makeGraph(names, dates, title))
            else:
                for personnage in personnages:
                    names = ["Debut recherche"]
                    dates = [form.cleaned_data["date_depart"]]
                    title = "Événements pour " + personnage.name + " " + years_between(
                        personnage, form.cleaned_data['date_depart'], form.cleaned_data['date_fin']) + " de " + _date(
                        form.cleaned_data['date_depart'], "d M Y") + " à " + _date(
                        form.cleaned_data['date_fin'], "d M Y")
                    for event in events.filter(date__range=(form.cleaned_data['date_depart'],
                                                            form.cleaned_data['date_fin'])).filter(personnages=personnage):
                        names.append(event.name)
                        dates.append(event.date)
                        if form.cleaned_data["flashback"] and event.flashback_date:
                            names.append(event.name + " flashback")
                            dates.append(event.flashback_date)

                    names.append("Fin recherche")
                    dates.append(form.cleaned_data["date_fin"])
                    graphics.append(makeGraph(names, dates, title))
    else:
        title = ""
        for event in Evenement.objects.all():
            names.append(event.name)
            dates.append(event.date)
        graphics.append(makeGraph(names, dates, title))

    form = SearchForm()
    return render(request, 'timeline/index.html', {'graphics': graphics, 'form': form})


def makeGraph(names, dates, title):
    # Choose some nice levels
    levels = np.tile([-5, 5, -4, 4, -3, 3, -2, 2, -1, 1],
                     int(np.ceil(len(dates) / 6)))[:len(dates)]

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(11, 8), constrained_layout=True)
    ax.set(title=title)

    markerline, stemline, baseline = ax.stem(dates, levels,
                                             linefmt="C3-", basefmt="k-",
                                             use_line_collection=True)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va in zip(dates, levels, names, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                    textcoords="offset points", va=va, ha="right")

    # format xaxis with 4 month intervals
    ax.get_xaxis().set_major_locator(ticker.AutoLocator())
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.margins(y=0.1)

    tmp = six.StringIO()
    fig.savefig(tmp, format='svg', bbox_inches='tight')
    plt.clf()

    return tmp.getvalue()


def years_between(personnage, d1, d2):
    age1 = int(abs((d1 - personnage.date_naissance)).days / 365)
    age2 = int(abs((d2 - personnage.date_naissance)).days / 365)

    return ("(" + str(age1) + "-" + str(age2)    + " ans)")
