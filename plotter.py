import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def plotLineChart(xdata, ydata, errdata, datalabel, xlabel, ylabel, title,
                  xlim=None, ylim=None, color="b", style="-", fileName=None):
    # NO VERIFICATIONS ARE DONE
    plt.figure()
    plt.errorbar(xdata, ydata, yerr=errdata, linewidth=3, linestyle=style, 
                 label=datalabel, color=color)

    axes = plt.gca()
    
    if xlim is not None:
        axes.set_xlim(xlim)
    else:
        offset = (max(xdata) - min(xdata)) * 0.1
        axes.set_xlim([min(xdata) - offset, max(xdata) + offset])

    if ylim is not None:
        axes.set_ylim(ylim)

    # Set the tick labels font
    for label in (axes.get_xticklabels() + axes.get_yticklabels()):
        label.set_fontsize(24)

    plt.xlabel(xlabel, fontsize=24)
    plt.ylabel(ylabel, fontsize=24)
    if title is not None:
        plt.title(title, fontsize=24)

    plt.tight_layout()

    if fileName is not None:
        plt.savefig(fileName, facecolor='w', transparent=True)
        plt.close()
    else:
        plt.show()


def plotMultLineChart(xdata, ydata, errdata, datalabels, xlabel, ylabel, title,
                      legendtitle=None, legendloc="a", xlim=None, ylim=None, 
                      fontsize=26, linewidth=3, fileName=None):
    # NO VERIFICATIONS ARE DONE
    plt.figure()
    plt.locator_params(axis='x', nbins=6)
    colors  = ['#387ef5', '#ef473a' , '#ffc900', '#33cd5f', "#000000"]
    styles  = ['-', '--', ':', '-.']
    markers = ["o", "s", "^", "x", "D", "*"]

    for i in range(0, len(ydata)):
        plt.errorbar(xdata[i], ydata[i], yerr=errdata[i], linewidth=linewidth,
                     linestyle=styles[i%len(styles)], label=datalabels[i], 
                     color=colors[i], marker=markers[i])

    axes = plt.gca()

    if xlim is not None:
        # axes.set_xlim(xlim)
        if xlim[0] is not None:
            axes.set_xlim(left=xlim[0])
        if xlim[1] is not None:
            axes.set_xlim(right=xlim[1])
    else:
        maxX = - float("inf")
        minX = float("inf")
        for xs in xdata:
            maxX = max(max(xs), maxX)
            minX = min(min(xs), minX)
        offset = (maxX - minX) * 0.1
        axes.set_xlim([minX - offset, maxX + offset])

    if ylim is not None:
        # axes.set_ylim(ylim)
        if ylim[0] is not None:
            axes.set_ylim(bottom=ylim[0])
        if ylim[1] is not None:
            axes.set_ylim(top=ylim[1])

    # Set the tick labels font
    for label in (axes.get_xticklabels() + axes.get_yticklabels()):
        label.set_fontsize(fontsize)
    
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    if title is not None:
        plt.title(title, fontsize=fontsize)

    if legendtitle is not None:
        ltitle = legendtitle
    else:
        ltitle = ""

    # if legendloc == "a":
    loc  = "best"
    bba  = None
    ncol = 1
    if legendloc == "u":
        # BAD
        loc = "upper center"
        ncol = len(ydata)
        box = axes.get_position()
        axes.set_position([box.x0, box.y0 + box.height * 0.1,
                           box.width, box.height * 0.9])
        bba = (1.05, 1)
    elif legendloc == "d":
        # BAD
        loc = "lower center"
        ncol = len(ydata)
        box = axes.get_position()
        axes.set_position([box.x0, box.y0 + box.height * 0.1,
                           box.width, box.height * 0.9])
        bba = (0.5, -0.05)

    if bba:
        legend = plt.legend(loc=loc, title=ltitle, bbox_to_anchor=bba, ncol=ncol, 
                            fontsize=fontsize)
    else:
        legend = plt.legend(loc=loc, title=ltitle, fontsize=fontsize-2)
        # legend = plt.legend(loc=loc, title=ltitle, fontsize=fontsize)

    if ltitle is not None:
        plt.setp(legend.get_title(), fontsize=fontsize-2)
        # plt.setp(legend.get_title(), fontsize=fontsize)

    plt.tight_layout()

    if fileName is not None:
        plt.savefig(fileName, facecolor='w', transparent=True)
        plt.close()
    else:
        plt.show()

def plotAreasChart(xdata, ydata, errdata, datalabels, xlabel, ylabel, title,
                   legendtitle=None, legendloc="a", xlim=None, ylim=None, 
                   fileName=None):
    # NO VERIFICATIONS ARE DONE
    plt.figure()
    # colors = ['#387ef5', '#ffc900', '#ef473a', '#33cd5f']
    # colors = ['#1485CC', '#FFFC19', '#B21212', '#33cd5f']
    colors = ['#0972B2', '#FFFC42', '#FF0003', '#33cd5f']
    styles = ['-', '--', ':', '-.']
    plt.stackplot(xdata, ydata, labels=datalabels, colors=colors)
    # for i in range(0, len(ydata)):
    #     plt.errorbar(xdata, ydata[i], yerr=errdata[i], linewidth=3,
    #                  linestyle=styles[i], label=datalabels[i], color=colors[i])

    axes = plt.gca()

    if xlim is not None:
        # axes.set_xlim(xlim)
        if xlim[0] is not None:
            axes.set_xlim(left=xlim[0])
        if xlim[1] is not None:
            axes.set_xlim(right=xlim[1])
        
    else:
        offset = (max(xdata) - min(xdata)) * 0.1
        axes.set_xlim([min(xdata) - offset, max(xdata) + offset])

    if ylim is not None:
        # axes.set_ylim(ylim)
        if ylim[0] is not None:
            axes.set_ylim(bottom=ylim[0])
        if ylim[1] is not None:
            axes.set_ylim(top=ylim[1])

    # Set the tick labels font
    for label in (axes.get_xticklabels() + axes.get_yticklabels()):
        label.set_fontsize(24)
    
    plt.xlabel(xlabel, fontsize=24)
    plt.ylabel(ylabel, fontsize=24)
    if title is not None:
        plt.title(title, fontsize=24)

    if legendtitle is not None:
        ltitle = legendtitle
    else:
        ltitle = ""

    # if legendloc == "a":
    loc  = "best"
    bba  = None
    ncol = 1
    if legendloc == "u":
        # BAD
        loc = "upper center"
        ncol = len(ydata)
        box = axes.get_position()
        axes.set_position([box.x0, box.y0 + box.height * 0.1,
                           box.width, box.height * 0.9])
        bba = (1.05, 1)
    elif legendloc == "d":
        # BAD
        loc = "lower center"
        ncol = len(ydata)
        box = axes.get_position()
        axes.set_position([box.x0, box.y0 + box.height * 0.1,
                           box.width, box.height * 0.9])
        bba = (0.5, -0.05)

    if bba:
        legend = plt.legend(loc=loc, title=ltitle, bbox_to_anchor=bba, ncol=ncol, 
                            fontsize=24)
    else:
        legend = plt.legend(loc=loc, title=ltitle, fontsize=24)
    if legendtitle is not None:
        plt.setp(legend.get_title(), fontsize=24)

    plt.tight_layout()

    if fileName is not None:
        plt.savefig(fileName, facecolor='w', transparent=True)
        plt.close()
    else:
        plt.show()