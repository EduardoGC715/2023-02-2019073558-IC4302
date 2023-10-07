
import styles from '../styles/Search.module.css';

export default function Facet({ value, text, onChange}) {
    return (
        <>
            <label className={styles.radioEngine}>
                <input
                type="checkbox"
                name="radioEngineGroup"
                checked={value}
                onChange={onChange}
                />
                {text}
            </label>
        </>
    )
}