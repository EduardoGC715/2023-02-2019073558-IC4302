
import styles from '../styles/Search.module.css';

export default function Facet({ key, name, value, text, onChange, facetObjectValue }) {
    return (
        <>
            <label className={styles.radioEngine}>
                <input
                type="radio"
                name={name}
                value={value}
                checked={facetObjectValue == value}
                onChange={onChange}
                />
                {text}
            </label>
        </>
    )
}