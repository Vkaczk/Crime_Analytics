import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def Navbar():
    LOGO = "assets/statics/esiee.png"
    items=[
        dbc.DropdownMenuItem("Gambier Délphine",href="https://www.linkedin.com/",external_link=True),
        dbc.DropdownMenuItem("Kaczmarczyk Victor",href="https://www.linkedin.com/in/victor-kaczmarczyk-747a85196/",external_link=True),
        ]
    navbar = dbc.Navbar(
                    [
                        #html.A(
                            # Use row and col to control vertical alignment of logo / brand
                            #dbc.Row(
                            #        [
                                    dbc.Col(html.A([html.Img(src=LOGO, height="50px")], href="https://www.esiee.fr"), width={"size":1}),
                                    dbc.Col(dbc.NavbarBrand("Projet Datasciences - Crimes Analytics", className="ml-2"), width={"size":10}),
                                    #dbc.Col(dbc.DropdownMenu(items,label="Auteurs",color='secondary', className="m-1",in_navbar=True,direction="right"), width={"size":1, "order": "last", "offset": 4})
                            #        ],
                            #        align="center",
                            #        no_gutters=True,
                            #        justify="beetwen"
                            #),
                            #href="https://junioresiee.com",
                            #),
                        dbc.DropdownMenu(items,label="Auteurs",color='secondary', className="m-1",in_navbar=True,direction="left")
                        #dbc.NavbarToggler(id="navbar-toggler"),
                        #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
                    ],
                color="dark",
                dark=True,
            )
    return navbar
