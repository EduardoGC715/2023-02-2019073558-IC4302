
import styles from '../styles/Search.module.css';
import Facet from './Facet';
import { Fragment } from 'react';

export default function FacetTable({ facetList, facetObject, handleFacetChange }) {

    const facetKeys = Object.keys(facetList);
    const fragments = facetKeys.map((key, index) => {
        const facetNames = facetList[key]['buckets'];
        return <Fragment key={`${key}`}>
                <p key={`${key}.${index}.Text`} className={styles.facetLabel}>{key}</p>
                <Facet key={`${key}.None`} name={key} value={"None"} text={"None"} onChange={e => handleFacetChange(e, key)} facetObjectValue={facetObject[key]}/>
                {
                    facetNames.map((facetJSON, indexFacet) => {
                        if (facetJSON['count']){
                            return <Facet key={`${key}.${facetJSON['_id']}`} name={key} value={facetJSON['_id']} text={facetJSON['_id']} onChange={e => handleFacetChange(e, key)} facetObjectValue={facetObject[key]}/>
                        }
                    })
                }
            </Fragment>
        
    })
    
    return (
        <div className={styles.facetTable}>
            <p className={styles.facetTitle}>Facet List</p>
            {fragments}
        </div>
    )
}

