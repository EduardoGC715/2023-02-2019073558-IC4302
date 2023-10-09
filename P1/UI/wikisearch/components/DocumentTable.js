
import styles from '../styles/Search.module.css';
import DocumentPreview from './DocumentPreview';
import { Fragment } from 'react';
import PropTypes from 'prop-types';

export default function DocumentTable({ documentList }) {

    const documentKeys = Object.keys(documentList);
    const documentComponents = documentKeys.map((doc) => <DocumentPreview key={documentList[doc]['_id']} doc={documentList[doc]}/>);
    return (
        <div className={styles.documentList}>
            <p className={styles.facetTitle}>Document List</p>
            {documentComponents}
        </div>
    )
}

DocumentTable.propTypes = {
    documentList: PropTypes.array.isRequired,
}