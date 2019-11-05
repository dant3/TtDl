import debugger


class VisitedUrlCache:
    def __init__(self):
        debugger.print('creating VisitedUrlCache obj')
        self.visited = set()
        debugger.print('visited = ', self.visited)

    def filter(self, lst):
        return [lnk for lnk in lst if lnk not in self.visited]

    def add(self, url):
        debugger.print('adding', url, 'to visited', self.visited)
        self.visited.add(url)
        debugger.print('added', url, 'to visited')
