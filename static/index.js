import {html, render, Component} from 'https://unpkg.com/htm/preact/standalone.mjs';
import Sockette from 'https://unpkg.com/sockette?module';
import Light from './Light.js';


class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            lights: []
        };

        this.onChange = this.onChange.bind(this);
        this.receiveChangeLight = this.receiveChangeLight.bind(this);
        this.receiveAddLight = this.receiveAddLight.bind(this);
        this.receiveMessage = this.receiveMessage.bind(this);
    }

    componentDidMount() {
        this.websocket = Sockette(
            'ws://127.0.0.1:8080/websocket',
            {
                onmessage: this.receiveMessage
            }
        );
    }
    componentWillUnmount() {
        this.websocket.close();
    }

    receiveMessage({data}) {
        data = JSON.parse(data);

        if (data['type'] === 'changeLight') {
            this.receiveChangeLight(data['light']);
        } else if(data['type'] === 'addLight') {
            this.receiveAddLight(data['light']);
        }
    }

    receiveChangeLight(newLight) {
        const {lights} = this.state;

        this.setState({
            lights: lights.map(
                light => light.id === newLight.id ? newLight : light
            )
        });
    }

    receiveAddLight(newLight) {
        const {lights} = this.state;
        
        // Don't add duplicate lights
        if(lights.some(
            ({id}) => id == newLight.id
        )) {
            return
        }

        this.setState({
            lights: [...lights, newLight]
        });
    }

    onChange(newLight) {
        const {lights} = this.state;
        this.setState({
            lights: lights.map(
                light => light.id === newLight.id ? newLight : light
            )
        });

        this.websocket.send(JSON.stringify({
            type: 'changeLight',
            light: newLight
        }));
    }

    render({}, {lights}) {
        return (
            html`
                <div>
                    ${lights.map(
                        light => html`
                            <${Light}
                                id=${light.id}
                                name=${light.name}
                                state=${light.state}
                                brightness=${light.brightness}
                                hue=${light.hue}
                                onChange=${this.onChange}
                            />
                        `
                    )}
                </div>
            `
        );
    }
}

render(
    html`
        <${App}/>
    `,
    document.body
)