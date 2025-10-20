"""@package musimath.note.Note
@author Kasper Rantamäki
Submodule for a generic note class
"""
from __future__ import annotations
from typing import Tuple, Optional
import matplotlib.pyplot as plt
import numpy as np

from ..constants import *


class Note:
  """Generic note class"""
  
  def __init__(self, frequency: float) -> None:
    """Constructor method
    
    Initializes a generic note with the given frequency
    
    @param frequency  The frequency of the note
    @return           None
    """
    self.__frequency = frequency  # Hertz

    n_octaves_from_standard = np.sign(frequency - standard_pitch) * np.floor(np.abs(np.log2(frequency / standard_pitch)))
    
    self.__octave = standard_octave + n_octaves_from_standard
    self.__base_frequency = self.__frequency * 2 ** (-self.__octave)  # Hertz
    self.__wavelength = speed_of_sound / self.__frequency  # Meters
    
  
  def __call__(self, t: float) -> float:
    """Call method
    
    Calling the note returns the value of the sinusoidal function that the note follows.
    Essentially gives the height of the vibration of a moving wave at some constant point
    at a given time. Note that all notes are normalized so that they have an amplitude of 1.
    
    @param t  The time from the beginning of the vibration in milliseconds 
    @return   The height of the vibration
    """
    return np.sin(2 * np.pi * self.frequency)
  
  
  def __str__(self) -> str:
    """String representation method
    
    Represents the note as a string
    
    @return  The note information as a string
    """
    return f"Base frequency: {self.base_frequency}\nOctave: {self.octave}\nFrequency: {self.frequency}"
  
  
  def __le__(self, other: Note) -> bool:
    """Less than or equal to comparison
    
    Notes are compared based on their frequency.
    
    @param other  Another note object
    @return       Boolean value telling if this note has smaller or equal frequency to the other
    """
    return self.frequency <= other.frequency
  
  
  def __le__(self, other: Note) -> bool:
    """Greater than or equal to comparison
    
    Notes are compared based on their frequency.
    
    @param other  Another note object
    @return       Boolean value telling if this note has greater or equal frequency to the other
    """
    return self.frequency >= other.frequency
  
  
  def __eq__(self, other: Note) -> bool:
    """Equal to comparison
    
    Notes are compared based on their frequency.
    
    @param other  Another note object
    @return       Boolean value telling if this note has equal frequency to the other
    """
    return self.frequency == other.frequency
  
  
  def __lt__(self, other: Note) -> bool:
    """Less than comparison
    
    Notes are compared based on their frequency.
    
    @param other  Another note object
    @return       Boolean value telling if this note has smaller frequency to the other
    """
    return self.frequency < other.frequency
  
  
  def __gt__(self, other: Note) -> bool:
    """Greater than comparison
    
    Notes are compared based on their frequency.
    
    @param other  Another note object
    @return       Boolean value telling if this note has greater frequency to the other
    """
    return self.frequency > other.frequency
  
  
  @property
  def octave(self) -> int:
    """The octave of the note
    
    Octaves denote the interval between two notes, where one note has twice the frequency of the other.
    Thus, the octaves of some base frequency can be found by multiplying it by $2^n$ where $n$ is the octave
    as an integer.
    
    @return  The octave
    """
    return self.__octave
  
  
  @property
  def base_frequency(self) -> float:
    """The base frequency of the note
    
    The frequency corresponding with octave 0.
    
    @return  The base frequency
    """
    return self.__base_frequency
  
  
  @property
  def frequency(self) -> float:
    """The frequency of the note
    
    The frequency of the note in the given octave
    
    @return  The frequency of the note
    """
    return self.__frequency
  
  
  @property
  def wavelength(self) -> float:
    """The wavelength of the note
    
    @return  The wavelength of the note
    """
    return self.__wavelength
  
  
  def half_step(self, n_steps: int) -> Note:
    """Half step note generator
    
    Method which generates a new note specified number of half steps away from this note
    
    @param n_steps  The number of half steps taken
    @return         Note the specified number of half steps away
    """
    return Note(self.frequency * 2 ** (n_steps / n_tets))


  def plot(self, x_range: Optional[Tuple[float, float]], 
           n_points: int = 100,
           x_label: Optional[str] = None, 
           y_label: Optional[str] = None, 
           ax: Optional[plt.Axes] = None, 
           **kwargs) -> plt.Axes:
    """Plotting method
    
    Plots the notes vibration as a function of time over the given interval.
    
    @param x_range          The space interval. Optional, defaults to a single wavelength
    @param n_points         The number of points plotted. Optional, defaults to 100
    @param x_label          The x axis label used in the Axes object. Optional, defaults to None (no label)
    @param y_label          The y axis label used in the Axes object. Optional, defaults to None (no label)
    @param ax               Pyplot Axes object to which the note will be plotted. Optional, defaults to None (new Axes created)
    @param **kwargs         Keyword arguments passed into the pyplot plot function
    @raises AssertionError  Raised if an invalid time interval is passed
    @return                 An pyplot.Axes object with the note plotted on it
    """
    if x_range is not None:
      assert x_range[0] < x_range[1], f"Invalid space interval! ({x_range[0]} > {x_range[1]})"
    else:
      x_range = (0, self.wavelength)
    
    if ax is None:
      ax = plt.axes()
      
    xx = np.linspace(x_range[0], x_range[1], n_points)
    yy = self(xx)  # Note that numpy functions should be used when defining the sinusoid
    
    ax.plot(xx, yy, **kwargs)
    
    if x_label is not None:
      ax.set_xlabel(x_label)
      
    if y_label is not None:
      ax.set_ylabel(y_label)
      
    return ax
      