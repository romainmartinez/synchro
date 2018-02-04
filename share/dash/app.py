import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


class Dash:
    def __init__(self, path2df, path2css):
        # get data
        self.df = self.get_data(path2df)
        # init app
        self.app = dash.Dash()

        self.header = self.set_header()

        self.dropdown = self.set_dropdown()

        self.app.layout = self.set_layout()

        self.set_css(path2css)

        # self.set_callbacks()

    @staticmethod
    def get_data(path2df):
        return pd.read_hdf(path2df)

    @staticmethod
    def set_header():
        text = '''
# Nage Synchronisée        

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
        '''
        header = html.Div([
            dcc.Markdown(children=text)
        ])
        return header

    def set_dropdown(self):
        dropdown = html.Div([
            dcc.Dropdown(
                id='my-dropdown',
                options=[{'label': index, 'value': index} for index in self.df.index],
                value=1
            ),
            html.Div(id='output-container')
        ])
        return dropdown

    def set_layout(self):
        layout = html.Div([
            self.header,
            self.dropdown
        ])
        return layout

    def set_callbacks(self):
        @self.app.callback(
            dash.dependencies.Output(component_id='output-container', component_property='children'),
            [dash.dependencies.Input(component_id='my-dropdown', component_property='value')]
        )
        def update_output(value):
            return f'You have selected {value}'

    def set_css(self, path2css):
        self.app.css.append_css({"external_url": path2css})


if __name__ == '__main__':
    DATA_FILENAME = '../../data/dataframe.hdf5'
    CSS_FILENAME = 'https://cdn.rawgit.com/romainmartinez/linux_scripts/c07de7d3/style_dash.css'
    obj = Dash(DATA_FILENAME, CSS_FILENAME)
    obj.app.run_server()
