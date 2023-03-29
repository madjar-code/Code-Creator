from itertools import islice, chain


class QuerySetChain:
    """
    Chains multiple subquerysets (possibly of differant models)
    a one queryset. Supports minimal methods needed for use with
    django.core.paginator.
    """
    
    def __init__(self, *subquerysets) -> None:
        self.querysets = subquerysets
    
    def count(self) -> int:
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        """Returns a clone of this queryset chain"""
        return self.__class__(**self.querysets)

    def _all(self):
        """Iterates records in all subquerysets"""
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from chained set of results from
        all subquerysets.
        """
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx + 1).__next__()
