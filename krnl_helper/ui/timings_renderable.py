from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class TimingsRenderable:
    def __init__(self, config):
        self.schedule = []
        self.current_time = 0

    def render(self, console, options):
        layout = Layout(name="schedule")

        table = Table(show_header=False, show_edge=False, expand=True)
        table.add_column("*", no_wrap=True, overflow="ellipsis")
        table.add_column("Title", no_wrap=True, overflow="ellipsis")
        table.add_column("Artist", no_wrap=True, overflow="ellipsis")
        table.add_column("Duration", no_wrap=True, overflow="ellipsis")
        panel = Panel(table, title="Schedule")
        layout.update(panel)

        rows = self._gen_rows()

        # This would also get the height:
        render_map = layout.render(console, options)
        n_rows = render_map[layout].region.height - 2

        while n_rows >= 0:
            table = Table(show_header=False, show_edge=False, expand=True)
            table.add_column("***", no_wrap=True, overflow="ellipsis")
            table.add_column("Title", no_wrap=True, overflow="ellipsis")
            table.add_column("Artist", no_wrap=True, overflow="ellipsis")
            table.add_column("Duration", no_wrap=True, overflow="ellipsis")

            for row in rows[-n_rows:]:
                table.add_row(*row)

            panel = Panel(table, title="Schedule")
            layout.update(panel)

            render_map = layout.render(console, options)

            if len(render_map[layout].render[-1]) > 2:
                # The table is overflowing
                n_rows -= 1
            else:
                break

        panel.height = render_map[layout].region.height

        return panel

    def __rich_console__(self, console, options):
        yield self.render(console, options)
