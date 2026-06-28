import plotly.express as px
from utils.logger import get_logger
log = get_logger(__name__)

class VisualizationAgent:
    def render(self, report):
        figures = {}
        for section_name, result in report.items():
            if not hasattr(result, "charts"):
                continue
            section_figures = []
            for chart in result.charts:
                try:
                    fig = self._create_chart(chart, report['dataframe'])
                    if fig is not None:
                        section_figures.append(fig)
                    
                except Exception as e:
                    log.warning(f"Unable to render chart: {e}")
            figures[section_name] = section_figures
        return figures
    
    def _create_chart(self, chart, df):
        chart_type = chart.get('type')
        if chart_type == 'histogram':
            return px.histogram(df, x = chart['column'], title= chart.get("title", chart['column']))
        elif chart_type == 'box':
            return px.box(df, y = chart['column'], title = chart.get("title", chart['column']))
        elif chart_type == 'scatter':
            return px.scatter(df, x = chart['x'], y = chart['y'], color = chart.get('color'))
        elif chart_type == 'bar':
            return px.bar(df, x = chart['x'], y = chart['y'], title =chart.get('title', ''))
        elif chart_type == 'heatmap':
            return px.imshow(chart['data'], text_auto = True, title = chart.get('title', 'Correlation'))
        
        return None
    
