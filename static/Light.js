import {html} from 'https://unpkg.com/htm/preact/standalone.mjs';

export default ({
    name,
    id,
    state,
    hue,
    brightness,
    onChange
}) => {
    const handleChange = change => onChange({
        id, state, hue, brightness, name, ...change
    });
    const handleChangeEvent = ({target}) => handleChange({
        [target.name]: target.type==='checkbox' ? target.checked : target.value
    });
    return (
        html`
            <div class="light">
                <h1>${name}</h1>
                <div class="light__state">
                    <input
                        type="checkbox"
                        name="state"
                        checked=${state}
                        id=${`${id}-state`}
                        onChange=${handleChangeEvent}
                    />
                    <label for=${`${id}-state`} aria-label="Toggle Power" titgle="Power">
                        <svg viewBox="-16 -16 32 32" width="100" height="100" stroke-width="3" stroke="currentColor" stroke-linecap="round" fill="none">
                            <circle cx="0" cy="0" r="13"/>
                            <line x1="0" x2="0" y1="-8" y2="8"/>
                        </svg>
                    </label>
                </div>
                <div class="light__hue">
                    <label for=${`${id}-hue`}>Hue</label>
                    <div class="hue-slider">
                        <input
                            type="range"
                            name="hue"
                            id=${`${id}-hue`}
                            min="0"
                            max="360"
                            value=${hue}
                            onChange=${handleChangeEvent}
                            
                        />
                    </div>
                </div>
                <div class="light__brightness">
                    <label
                        for=${`${id}-brightness`}
                    >Brightness</label>
                    <div class="light__brightness__inner">
                        <label
                            for=${`${id}-brightness`}
                            aria-label="Lower Brightness"
                            onClick=${() => handleChange({
                                brightness: Math.max(1, brightness - 10)
                            })}
                        >\uD83D\uDD05</label>
                        <input
                            type="range"
                            min="1"
                            max="100"
                            name="brightness"
                            id=${`${id}-brightness`}
                            value=${brightness}
                            onChange=${handleChangeEvent}
                            aria-label="Brightness"
                        />
                        <label
                            for=${`${id}-brightness`}
                            aria-label="Raise Brightness"
                            onClick=${() => handleChange({
                                brightness: Math.min(100, brightness + 10)
                            })}
                        >\uD83D\uDD06</label>
                    </div>
                </div>
            </div>
        `
    );
}