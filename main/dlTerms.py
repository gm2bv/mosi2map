class dlTerms:
    """a simple class to describe terms of events.
    """
    
    items = [
        {'min':0, 'val':"--"},
        {'min':15, 'val':"15分"},
        {'min':30, 'val':'30分'},
        {'min':60, 'val':'1時間'},
        {'min':120, 'val':'2時間'},
        {'min':240, 'val':'4時間'},
        {'min':720, 'val':'半日'},
        {'min':1440, 'val':'終日'}
    ]

    def selectMin(self, min):
        for v in self.items:
            if v['min'] == int(min):
                v['selected'] = 'selected'

    def getVal(self, min):
        ret = 0
        for v in self.items:
            if v['min'] == int(min):
                ret = v['val']
                break
        return ret
    


                
