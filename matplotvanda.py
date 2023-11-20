# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import itertools
import matplotlib.ticker as ticker

def mostrar_ejes(axis, eje='x'):
    '''
    Añade los ejes coordenados a un subplots.

    Parámetros
    ----------
    axis : matplotlib Axes
        Axis sobre el cual mostrar los ejes.
    eje : str
        Eje a mostrar. Por defecto es 'x'.
    '''
    y_spine = axis.spines['left']
    lc = y_spine.get_edgecolor()
    lw = y_spine.get_linewidth()
    ls = y_spine.get_linestyle()

    #Me fijo si el eje es válido
    ejes = [''.join(p) for i in range(1,3) for c in itertools.combinations('xy',i)
     for p in itertools.permutations(''.join(c))]
    
    if eje not in ejes:
        raise TypeError('Eje(s) no válido(s)')
    if 'x' in eje:
        axis.axhline(0, color=lc, lw=lw, ls=ls)
    if 'y' in eje:
        axis.axvline(0, color=lc, lw=lw, ls=ls)
        
def agregar_tick(axis, valor, label, eje='x', gridline=True):
    if eje=='x':
        ax = axis.xaxis
    elif eje=='y':
        ax = axis.yaxis
    elif eje=='z':
        ax = axis.zaxis
    else:
        raise TypeError('El eje ingresado es invalido')
    ticks = list(ax.get_ticklocs())+[valor]
    labels = list(ax.get_ticklabels())+[label]
    ax.set_ticks(ticks, labels=labels)
    if not gridline:

        if eje=='x':
            gridlines = axis.get_xgridlines()
            vals = [line.get_xdata()[0] for line in gridlines]
        elif eje=='y':
            gridlines = axis.get_ygridlines()
            vals = [line.get_ydata()[0] for line in gridlines]
        elif eje=='z':
            gridlines = axis.get_zgridlines()
            vals = [line.get_zdata()[0] for line in gridlines]
        for (line, val) in zip(gridlines, vals):
            if val == valor:
                line.set_visible(False)
        
def sacar_ticklabel(axis, valor, eje='x'):
    if eje=='x':
        ax = axis.xaxis
        i = 0
    elif eje=='y':
        ax = axis.yaxis
        i = 1
    elif eje=='z':
        ax = axis.zaxis
        i = 2
    else:
        raise TypeError('El eje ingresado es invalido')
    labels = [text if text.get_position()[i]!=valor else '' for text in ax.get_ticklabels()]
    ax.set_ticklabels(labels)

def marcar_punto(axis, punto, labels, eje='xy', ls='--', marker=True, zorder=None):
    y_spine = axis.spines['left']
    lc = y_spine.get_edgecolor()
    lw = y_spine.get_linewidth()
    flecha = dict(arrowstyle = '-', lw=lw,
              color=lc, ls=ls)

    #Me fijo si el eje es válido
    ejes = [''.join(p) for i in range(1,3) for c in itertools.combinations('xy',i)
     for p in itertools.permutations(''.join(c))]
    
    if eje not in ejes:
        raise TypeError('Eje(s) no válido(s)')
        
    if 'x' in eje:
        agregar_tick(axis, punto[0], labels[0], eje='x', gridline=False)
        anotación_x = axis.annotate('', punto, (punto[0],0), xycoords='data',
                                textcoords=('data','axes fraction'),
                                arrowprops=flecha, zorder=zorder)
        
    if 'y' in eje:
        agregar_tick(axis, punto[1], labels[1], eje='y', gridline=False)
        anotación_y = axis.annotate('', punto, (0,punto[1]), xycoords='data',
                                textcoords=('axes fraction','data'),
                                arrowprops=flecha, zorder=zorder)

    if marker:
        [marker] = axis.plot(*punto, marker='.', markerfacecolor=lc, markeredgecolor=lc)
    #return anotación_x, anotación_y, marker
    
def gula_grid(ax):
    '''
    Crea grilla estética sobre un subplot.

    Parameters
    ----------
    ax : matplotlib Axes
        Axis sobre el cual aplicar la grilla.
    '''
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.grid(True, alpha=.6)
    ax.grid(True, which='minor', ls='--', alpha=.3)

def grid_subplots(*args, **kwargs):
    '''
    Crea subplots con grilla estética. Mismos argumentos que plt.subplots().
    '''
    fig, axs = plt.subplots(*args, **kwargs)
    try:
        for ax in axs.flat:
            gula_grid(ax)
    except:
        gula_grid(axs)
    return fig, axs

def cambiar_unidades(ax, eje, n):
    '''
    Cambia las unidades de las etiquetas del eje (no los datos) según la potencia
    n-ésima de 10.

    Parámetros
    ----------
    ax : matplotlib Axes
        Axis sobre el cuál se cambian las unidades.
    eje : str
        Eje sobre el cuál se cambian las unidades. 'x' o 'y'.
    n : int
        Orden de la potencia de 10 según la cuál se hace el cambio.
    '''
    if type(n) != int:
        raise TypeError('El orden de la potencia de 10 es inválido')
    if eje=='x':
        axis = ax.xaxis
    elif eje=='y':
        axis = ax.yaxis
    elif eje=='z':
        axis = ax.zaxis
    else:
        raise TypeError('El eje introducido es inválido')
    axis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*10**n)))