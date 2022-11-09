

class VirtualIndex:
    VIRTUAL_INDEX={'person': ((0.0, 0.999999, 1), (1.0, 1.999999, 2), (2.0, 5.0, 3)), 'car': ((0.0, 1.999999, 1), (2.0, 4.999999, 2), (5.0, 10.0, 3)), 'bicycle': ((0.0, 0.999999, 1), (1.0, 3.0, 2)), 'bus': ((0.0, 1.0, 1),), 'truck': ((0.0, 0.999999, 1), (1.0, 2.0, 2)), 'motorbike': ((0.0, 1.0, 1),), 'traffic light': ((0.0, 0.999999, 1), (1.0, 3.0, 2)), 'speed': ((0.0, 9.222959000000001, 1), (9.22296, 24.075999, 2), (24.076, 40.31804, 3))}
 
    @classmethod
    def keys(cls):
        return cls.VIRTUAL_INDEX.keys()
    
    @classmethod
    def bins(cls):
        return cls.VIRTUAL_INDEX