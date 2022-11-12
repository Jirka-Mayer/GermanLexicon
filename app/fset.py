import itertools


class fset:
    """Like set, but contains frequency for each word"""
    def __init__(self, enumerable=[]):
        self._items = {}
        self.add_many(enumerable)

    def add(self, item):
        if item not in self._items:
            self._items[item] = 1
        else:
            self._items[item] += 1

    def add_many(self, enumerable):
        for i in enumerable:
            self.add(i)

    def remove_one(self, item):
        if item not in self._items:
            return False
        else:
            self._items[item] -= 1
            if self._items[item] <= 0:
                del self._items[item]
            return True

    def remove_all(self, item):
        if item not in self._items:
            return False
        del self._items[item]
        return True

    def __contains__(self, item):
        return item in self._items

    def __getitem__(self, item):
        if item in self._items:
            return self._items[item]
        return 0

    def __delitem__(self, item):
        self.remove_all(item)

    def __iter__(self):
        return iter(
            k for k, v in sorted(
                self._items.items(),
                key=lambda i: i[1],
                reverse=True
            )
        )

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return "{\n  " + ",\n  ".join(
            repr(k) + ": " + repr(v) for k, v in
            itertools.islice(
                sorted(
                    self._items.items(),
                    key=lambda i: i[1],
                    reverse=True
                ),
                100
            )
        ) + "\n  ...\n}"
