import {html, render, Component} from 'https://unpkg.com/htm/preact/standalone.mjs';
import Sockette from 'https://unpkg.com/sockette?module';
import Light from './Light.js';


class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            lights: [
                {
                    id: 'light.alpha',
                    name: 'Alpha Bulb',
                    state: true,
                    brightness: 75,
                    color: 'red'
                },
                {
                    id: 'light.beta',
                    name: 'Beta Bulb',
                    state: false,
                    brightness: 50,
                    color: 'red'
                }
            ]
        };

        this.onChange = this.onChange.bind(this);
        this.receiveChange = this.receiveChange.bind(this);
    }

    componentDidMount() {
        this.websocket = Sockette(
            'ws://127.0.0.1:5000/websocket',
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
        console.log(newLight);
        this.setState({
            lights: lights.map(
                light => light.id === newLight.id ? (
                    {...light, ...newLight}
                ) : light
            )
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
                                state=${light.state}
                                brightness=${light.brightness}
                                color=${light.color}
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