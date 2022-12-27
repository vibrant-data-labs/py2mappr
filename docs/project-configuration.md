# Project Configuration

`OpenmapprProject` object is the main object to create and manage a project. It provides the API to create a project, add data, add layouts, add network, and publish the project.

## Project settings

Project settings are the global settings for the project.

The project settings could be updated by directly changing the `.configuration` dictionary or by using utility methods, provided by `OpenmapprProject` object:

        project.configuration.update({
            "headerTitle": "My project"
        })

        # or

        project.set_display_data(title="My project")

The following settings are available:

| Name | Data Type | Default Value | Description |
| ----------- | ----------- | ----------- | ----------- |
| `fontClass` | str | `Roboto` | The font to be used in the project. Modifying this field requires to include fonts in the `index.html` |
| `showStartInfo` | Boolean | `True` | Whether to display the project infromation on the start |
| `showHeader` | Boolean | `True` | Whether to display the project header |
| `headerType` | str `simple / html` | `simple` | Defines the type of the header in the project. In the case of `html` requires `headerTitle` and/or `headerHtml` to be set |
| `headerTitle` | str | `map title` | The title to be used in the project |
| `headerHtml` | str, html, markdown | `<h1>map header</h1>` | The Header content to be used in the project, if `headerType == 'html'` |
| `displayExportButton` | Boolean | `False` | Whether to allow SVG export of the layout |
| `modalDescription` | str, html, markdown | `<p>map description</p>` | Defines the HTML with information about the project |
| `modalSubtitle` | str, html, markdown | `<p>map subtitle</p>` | Defines the HTML with project subtitle |
| `displayTooltipCard` | Boolean | `False` | Whether to render a card, when hovering attribute in the list panel |
| `startPage` | str `legend / filter / list` | `legend` | Defines the panel on the left-hand side to be rendered first |
| `defaultPanel` | str  | `Map Information` | The title of the right panel |
| `projectLogoTitle` | str  | `openmappr network exploration tool` | The title of the project in the header |
| `projectLogoUrl` | str | - | Displays the image of the project |
| `beta` | Boolean | `False` | Displays the 'beta' ribbon |
| `sponsorsTxt` | str | `Sponsored by` | Defines the custom text for sponsors block |
| `sharingLogoUrl`| str | - | URL of the image to be included in the sharing post |
| `socials` | array of strings `linkedin / twitter / facebook` | empty array | Defines the social networks, which will be rendered in the 'Share' panel |
| `sponsors` | array of objects | empty array | See below |
| `footer` | object | `None` | See below |
| `feedback` | object | - | See below |

### `sponsors`

Sponsors array contains objects with the following fields:
* `iconUrl` - the url of the sponsor's logo
* `linkUrl` - the url of the sponsor's website
* `linkTitle` - the title of the sponsor

e.g. it can be defined as follows:

```json
"sponsors": [
    {
        "iconUrl": "https://mappr-player.openmappr.org/img/logos/vdl-logo.svg",
        "linkUrl": "https://www.vibrantdatalabs.org/",
        "linkTitle": "Vibrant Data Labs"
    },
]
```

### `footer`

Footer objects allows to customize the footer of the right info panel. It contains the following fields:

* `studioLogo` - the url of the studio logo
* `studioName` - the name of the studio
* `studioLink` - the url of the studio website

### `feedback`

This section allows to customize the feedback form. It contains the following fields:

* `type` - the type of the feedback form. It could be either `email` or `link`
* `link` - the url of the feedback form. In the case of `type == 'email'` it should be the email address, as in the player it will be prepended with `mailto:`
* `text` - the text to be displayed in the feedback button

## Shortcut methods

`OpenmapprProject` object provides a set of methods to simplify the modification of the settings.

#### `set_display_data`

This method allows to set the following settings `headerTitle`, `projectLogoTitle`, `modalSubtitle`, `projectLogoUrl`, `sponsorsTxt`, `modalDescription`.

        project.set_display_data(
            title="My Project",
            description="<p>My project description</p>", 
            logo_image_url="https://myimage.com/image.png")

#### `set_feedback`

This method allows to set the `feedback` field of the project.

        project.set_feedback({
                "type": "link",
                "link": "https://myfeedbackform.com",
                "text": "Please leave feedback!"
            })

#### `set_export_button`

This method allows to set the `displayExportButton` field of the project.

        project.set_export_button(True)

#### `set_socials`

It allows to define a set of social networks, where the sharing is possible:

        project.set_socials(["linkedin", "twitter"])

#### `create_sponsor_list`

It accepts the sponsors tuples and appends the data to the configuration:

        project.create_sponsor_list([
            ("My Sponsor", "https://mylogo.com/logo.png", "https://mysponsor.com"),
            ("My Sponsor 2", "https://mylogo2.com/logo.png", "https://mysponsor2.com")
        ])

#### `set_beta`

Enables the `beta` ribbon:

        project.set_beta()

