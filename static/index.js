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
        this.receiveChange = this.receiveChange.bind(this);
    }

    componentDidMount() {
        this.websocket = Sockette(
            // 'wss://serene-springs-30122.herokuapp.com/websocket',
            'ws://127.0.0.1:8080/websocket',
            {
                onmessage: this.receiveChange
            }
        );
    }
    componentWillUnmount() {
        this.websocket.close();
    }

    receiveChange({data}) {
        const newLight = JSON.parse(data);
        const {lights} = this.state;
        const isUpdate = lights.some(light => light.id === newLight.id);

        const newLights = isUpdate ? (
            lights.map(
                light => light.id === newLight.id ? (
                    {...light, ...newLight}
                ) : light
            )
        ) : [
            ...lights, newLight
        ];

        this.setState({
            lights: newLights
        });
    }

    onChange(newLight) {
        const {lights} = this.state;
        this.setState({
            lights: lights.map(
                light => light.id === newLight.id ? newLight : light
            )
        });

        this.websocket.send(JSON.stringify(newLight));
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