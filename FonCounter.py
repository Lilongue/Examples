#pylint:disable=C0301
#pylint:disable=C0103
"""
Classes for fon count on bpu
"""

#Import section
#import scipy as sp
from collections import deque

class SlideCount(object):
    """
    Class for the sliding counting
    """
    def __init__(self, bd_number, slide_number):
        self.bd_number = bd_number
        self.slide_number = slide_number
        self.count_array = []
        for i in range(bd_number):
            self.count_array.append(deque([],slide_number))
        
    def put_count(self, count):
        """
        Putting count array
        """
        for i in range(self.bd_number):
            self.count_array[i].append(count[i])
        return  True
   
    @property
    def is_full(self):
        """
        Show if array is full
        """
        if len(self.count_array[0]) == self.slide_number:
            return True
        return False
        
    @property
    def is_empty(self):
        """
        Show if array is empty
        """
        if not self.count_array[0]:
            return True
        return False
        
    def __str__(self):
        out_str = ""
        for dq in self.count_array:
            out_str += str(list(dq)) + "\r\n"
        return out_str
        
    def clear(self):
        """
        Clearing all data from count array
        """
        for dq in self.count_array:
            dq.clear()
    
    @property
    def integral(self):
        """
        Returns the tuple of the sums of count for each channel
        """
        sums = []
        for dq in self.count_array:
            a = 0
            for i in dq:
                a += i
            sums.append(a)
        return tuple(sums)
        
    @property
    def average(self):
        """
        Return the average mean of count for all channels
        """
        ever = list(self.integral)
        for i,e in enumerate(ever):
            ever[i] = round(e/len(self.count_array[0]),3)
        return tuple(ever)


class BufferCount(object):
    """
    Buffering and returns the tuples of count
    """
    def __init__(self, size, return_type = 1):
        self.size = size
        self.return_type = return_type
        self.buffer = deque([], size)
   
    @property
    def is_full(self):
        """
        Shows if buffer is full
        """
        if len(self.buffer) == self.size:
            return True
        return False
    
    @property
    def integral(self):
        """
        Returns the sum of buffer
        """
        summ = 0
        for i in self.buffer:
            summ += i
        return summ
        
    def clear(self):
        """
        Clearing the buffer
        """
        self.buffer = deque([],self.size)
        
    def put_count(self, count):
        """
        Putting count array.
        Returns None if array is not full
        Returns tuple of counts, if return_tupe == 1
        Returns sum of array values, if return_type == 2
        """
        self.buffer.append(count)
        if self.is_full:
            if self.return_type == 2:
                tmp = self.integral
            if self.return_type == 1:
                tmp = tuple(self.buffer)
            self.clear()
            return tmp
        return None
        
class BufferCountA(BufferCount):
    """
    class for buffering lists of values with single value input.
    For example you can get list of sums by two from 8 single values.
    in: 1, 1, 1, 2, 1, 1, 1, 3 gives
    out: (2, 2, 2, 5)
    """
    
    def __init__(self, size, times):
        BufferCount.__init__(self,size)
        self.times = times
        self.counter = SlideCount(size,times)
        
    def put_count(self, count):
        """
        Putting count in array.
        Returns None if array is not full
        Returns tuple of counts if aray if full
        """
        tmp = None
        self.buffer.append(count)
        if self.is_full:
            self.counter.put_count(list(self.buffer))
            self.clear()
        if self.counter.is_full:
            tmp = self.counter.integral
            self.counter.clear()
        return tmp

class FonCounter(object):
    """
    Class for counting of fon and work count
    """
    
    @classmethod
    def count_fromdelta(cls, length, delta):
        """
        Return count of deltas in len or None, if this is not possible
        """
        if (length * 100 % int(delta*100)) == 0:
            return int(length / delta)
        return None
    
    def __init__(self, bd_number, delta, start_fon=None):
        self.bd_number = bd_number
        self.delta = delta
        self._ticks = 0
        if start_fon is None:
            self.start_fon = None
        else:
            self.start_fon = start_fon
            self.fill_fon(start_fon)
        
        #section of parameters initiation
        self.fon_podinterval = delta
        self.fon_times = 1
        self.count_work = 1
        self.can_count = True
        self.can_fon = True
        self.fon_subarray = -1
        self.fon_array = -1
        self.count_array = -1
        self.is_init = False
        
    def start_init(self, fon_podinterval, fon_times, count_work):
        """
        Initiation of fon and count arrays
        """
        self.fon_podinterval = fon_podinterval
        self. fon_times = fon_times
        self.count_work = count_work
        if FonCounter.count_fromdelta(fon_podinterval,self.delta) is None:
            raise IOError("Fon podinterval is not devide by delta")
        self.fon_subarray = SlideCount(self.bd_number,FonCounter.count_fromdelta(fon_podinterval,self.delta))
        self.fon_array = SlideCount(self.bd_number,fon_times)
        self.count_array = SlideCount(self.bd_number,self.count_work)
        self.is_init = True

    def fill_fon(self, number):
        """[Filling fon arrays with fix values that calculates as "number/self.count_work"]
        
        Arguments:
            number {[integer]} -- [fon in the work interval]
        
        """
        while not self.fon_array.is_full:
            while not self.fon_subarray.is_full:
                self.fon_subarray.put_count(number/self.count_work)
            self.fon_update()
        
    def push(self, count):
        """
        Method, that pushing the data to the all class arrays
        It must be in iterable format, with len in oder the bd_count
        If format is wrong, method raise an IOError Exception
        If method start_init() was
        """
        if not self.is_init:
            raise RuntimeError("Class not init. Call self.start_init() first")
        if len(count) != self.bd_number:
            raise IOError("Input data format is wrong")
        self._ticks += 1
        if self.can_count:
            self.fon_subarray.put_count(count)
        if self.can_fon:
            self.count_array.put_count(count)
        if self.fon_subarray.is_full:
            return True
        return  False
        
    @property
    def tick(self):
        """
        Returns the current ticks number
        """
        return self._ticks
    
    def fon_update(self):
        """
        Method updating the fon count.
        It put count from fon subinterval array to fon main array.
        Fon subinterval array is clearing.
        """
        self.fon_array.put_count(self.fon_subarray.integral)
        self.fon_subarray.clear()
        
    def is_fon_ready(self):
        """
        Show if the fon interval is full
        """
        return self.fon_array.is_full
        
    @property
    def fon_work(self):
        """
        Property, that returns fon if the fon array is not empty.
        Return None, if the fon array is empty
        """
        if not self.fon_array.is_empty:
            out_tup = list(self.fon_array.average)
            for i,dq in enumerate(out_tup):
                out_tup[i] = (dq/FonCounter.count_fromdelta(self.fon_podinterval,self.delta)*self.count_work)
            return tuple(out_tup)
        return  None
      
    @property
    def count(self):
        """
        Return the integral count if it is ready.
        Return None if the count array is not full.
        """
        if not self.count_array.is_full:
            return None
        return self.count_array.integral
        
    def fon_clear(self):
        """
        Clearing fon arrays
        """
        self.fon_array.clear()
        self.fon_subarray.clear()
        
    def subfon_clear(self):
        """
        Clearing fon subarray
        """
        self.fon_subarray.clear()
        
    def count_clear(self):
        """
        Clearing the count array
        """
        self.count_array.clear()
    
    def stop_count(self):
        """
        Stops the count filling and clearing the count array
        """
        self.count_array.clear()
        self.can_count = False
        
    def run_count(self):
        """
        Runs the count array filling
        """
        self.can_count = True
        
    def  stop_fon(self):
        """
        Stops the fon counting, and clearing the fon subinterval array.
        Fon array is not clearing!
        """
        self.fon_subarray.clear()
        self.can_fon  = False
        
    def run_fon(self):
        """
        Running the fon array filling
        """
        self.can_fon = True


class FonCounterAuto(FonCounter):

    def __init__(self, bd_number, delta, start_fon=None):
        FonCounter.__init__(self,bd_number,delta,start_fon)

    def push(self,count):
        """
        Method, that pushing the data to the all class arrays
        It must be in iterable format, with len in oder the bd_count
        If format is wrong, method raise an IOError Exception
        If method start_init() was
        """
        if not self.is_init:
            raise RuntimeError("Class not init. Call self.start_init() first")
        if len(count) != self.bd_number:
            raise IOError("Input data format is wrong")
        if self.can_count:
            self.fon_subarray.put_count(count)
        if self.can_fon:
            self.count_array.put_count(count)
        if self.fon_subarray.is_full:
            self.fon_update()
        return  False

        