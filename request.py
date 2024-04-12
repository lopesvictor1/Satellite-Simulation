class Request:
    def __init__(self, name: int, processing_capacity: int, time_needed: int):
        self.name = name
        self.processing_capacity = processing_capacity
        self.time_needed = time_needed
        self.satellite = None
        self.done = False
        
    def reduce_execution_time(self):
        '''
        Reduce the execution time of the request by 1 second.
        
        Required: self.time_needed (int): The time needed for the request in seconds.
        Returns: Updates the time_needed attribute of the request.
        '''
        self.time_needed -= 1
        if self.time_needed == 0:
            self.done = True
    
    def assign_satellite(self, satellite):
        '''
        Assign a satellite to the request.
        
        Required: satellite (Satellite): The satellite to assign to the request.
        Returns: Updates the satellite attribute of the request.
        '''
        self.satellite = satellite
        
    def release_satellite(self):
        '''
        Release the satellite from the request.
        
        Required: None
        Returns: Updates the satellite attribute of the request.
        '''
        self.satellite = None