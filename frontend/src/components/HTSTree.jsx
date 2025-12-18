import React, { useState, useEffect } from 'react';
import './HTSTree.css';

const TreeNode = ({ node }) => {
    const [expanded, setExpanded] = useState(false);
    const hasChildren = node.children && node.children.length > 0;

    return (
        <div className="tree-node">
            <div
                className={`node-header ${expanded ? 'expanded' : ''}`}
                onClick={() => setExpanded(!expanded)}
            >
                <span className="node-icon">{hasChildren ? (expanded ? '−' : '+') : '•'}</span>
                <span className="node-label">{node.name || node.full_name} {node.hts_code ? `(${node.hts_code})` : ''}</span>
            </div>
            {expanded && hasChildren && (
                <div className="node-children">
                    {node.children.map((child, idx) => (
                        <TreeNode key={idx} node={child} />
                    ))}
                </div>
            )}
        </div>
    );
};

const HTSTree = () => {
    const [treeData, setTreeData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/tree')
            .then(res => res.json())
            .then(data => {
                setTreeData(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to load tree", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="tree-loading">Loading Hierarchy...</div>;

    return (
        <div className="hts-tree-container">
            <h3>Navigating the TN VED tree</h3>
            <div className="tree-root">
                {treeData.map((node, idx) => (
                    <TreeNode key={idx} node={node} />
                ))}
            </div>
        </div>
    );
};

export default HTSTree;
