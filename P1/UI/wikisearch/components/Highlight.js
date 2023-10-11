
import styles from '../styles/Highlight.module.css'

export default function Highlight({ highlight }){

    const highlightKeys = Object.keys(highlight);
    const highlights = highlightKeys.map((index) => {
            if (highlight[index]['type'] == 'text'){
                return <span className={styles.normalText}>{highlight[index]['value']}</span>
            } else {
                return <span className={styles.highlightText}>{highlight[index]['value']}</span>
            }
        });
    return (
        <>
            {highlights}
        </>
    )
}