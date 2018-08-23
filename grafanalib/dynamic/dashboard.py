
import attr
import itertools
import math
import pdb
from numbers import Number
from grafanalib.dynamic.core import *
from jinja2 import Environment, PackageLoader

@attr.s
class Dashboard(object):

    title = attr.ib()
    rows = attr.ib()
    annotations = attr.ib(
        default=Annotations(),
        validator=attr.validators.instance_of(Annotations),
    )
    editable = attr.ib(
        default=True,
        validator=attr.validators.instance_of(bool),
    )
    gnetId = attr.ib(default=None)
    hideControls = attr.ib(
        default=False,
        validator=attr.validators.instance_of(bool),
    )
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    refresh = attr.ib(default=DEFAULT_REFRESH)
    schemaVersion = attr.ib(default=SCHEMA_VERSION)
    sharedCrosshair = attr.ib(
        default=False,
        validator=attr.validators.instance_of(bool),
    )
    style = attr.ib(default=DARK_STYLE)
    tags = attr.ib(default=attr.Factory(list))
    templating = attr.ib(
        default=Templating(),
        validator=attr.validators.instance_of(Templating),
    )
    time = attr.ib(
        default=DEFAULT_TIME,
        validator=attr.validators.instance_of(Time),
    )
    timePicker = attr.ib(
        default=DEFAULT_TIME_PICKER,
        validator=attr.validators.instance_of(TimePicker),
    )
    timezone = attr.ib(default=UTC)
    version = attr.ib(default=0)

    def _iter_panels(self):
        for row in self.rows:
            for panel in row._iter_panels():
                yield panel

    def _map_panels(self, f):
        return attr.evolve(self, rows=[r._map_panels(f) for r in self.rows])

    def auto_panel_ids(self):
        """Give unique IDs all the panels without IDs.

        Returns a new ``Dashboard`` that is the same as this one, except all
        of the panels have their ``id`` property set. Any panels which had an
        ``id`` property set will keep that property, all others will have
        auto-generated IDs provided for them.
        """
        ids = set([panel.id for panel in self._iter_panels() if panel.id])
        auto_ids = (i for i in itertools.count(1) if i not in ids)

        def set_id(panel):
            return panel if panel.id else attr.evolve(panel, id=next(auto_ids))
        return self._map_panels(set_id)

    def set_title(self, title):
        self.title=title

    def set_tags(self, tags):
        self.tags=tags

    def to_json_data(self, to_push_via_rest=False):
        if self.refresh is not False:
            tmp_json = {
                'annotations': self.annotations,
                'editable': self.editable,
                'gnetId': self.gnetId,
                'hideControls': self.hideControls,
                'id': self.id,
                'links': self.links,
                'refresh': self.refresh,
                'rows': self.rows,
                'schemaVersion': self.schemaVersion,
                'sharedCrosshair': self.sharedCrosshair,
                'style': self.style,
                'tags': self.tags,
                'templating': self.templating,
                'title': self.title,
                'time': self.time,
                'timepicker': self.timePicker,
                'timezone': self.timezone,
                'version': self.version,
            } 
        else:
            tmp_json = {
                'annotations': self.annotations,
                'editable': self.editable,
                'gnetId': self.gnetId,
                'hideControls': self.hideControls,
                'id': self.id,
                'links': self.links,
                'rows': self.rows,
                'schemaVersion': self.schemaVersion,
                'sharedCrosshair': self.sharedCrosshair,
                'style': self.style,
                'tags': self.tags,
                'templating': self.templating,
                'title': self.title,
                'time': self.time,
                'timepicker': self.timePicker,
                'timezone': self.timezone,
                'version': self.version,
            } 
        if(to_push_via_rest):
            tmp_json = {
                        "dashboard": tmp_json,
                        "overwrite": True
                        }
        
        return(tmp_json)
