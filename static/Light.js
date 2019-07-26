import {html} from 'https://unpkg.com/htm/preact/standalone.mjs';

export default ({
    name,
    id,
    state,
    color,
    brightness,
    onChange
}) => {

    const handleChange = ({target}) => onChange({
        id, state, color, brightness,
        [target.name]: target.type==='checkbox' ? target.checked : target.value
    });
    return (
        html`
            <div>
                <h1>${name}</h1>
                <label>
                    On
                    <input
                        type="checkbox"
                        name="state"
                        checked=${state}
                        onChange=${handleChange}
                    />
                </label>
                <label for=${`${id}-color`}>Color</label>
                <input
                    type="color"
                    name="color"
                    id=${`${id}-color`}
                    value=${color}
                    onChange=${handleChange}
                />
                <label for=${`${id}-brightness`}>Brightness</label>
                <input
                    type="range"
                    min="0"
                    max="100"
                    name="brightness"
                    id=${`${id}-brightness`}
                    value=${brightness}
                    onChange=${handleChange}
                />
            </div>
        `
    );
}