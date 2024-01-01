/**
 * These definitions are all provided by Azure.
 * @typedef {Object} X509Thumbprint
 * @property {string} primaryThumbprint
 * @property {string} secondaryThumbprint
 * 
 * @typedef {Object} TwinProperties
 * @property {Object.<string, any>} reported - The reported properties
 * @property {Object.<string, any>} desired - The desired properties
 * 
 * @typedef {Object.<string, any>} TwinTags
 * TODO - what structure does this object have?
 * 
 * @typedef {Object} Twin
 * @property {string} deviceId
 * @property {string} moduleId
 * @property {string} etag
 * @property {string} deviceEtag
 * @property {string} status
 * @property {string} statusUpdateTime
 * @property {string} connectionState
 * @property {string} lastActivityTime
 * @property {string} cloudToDeviceMessageCount
 * @property {string} authenticationType
 * @property {X509Thumbprint} x509Thumbprint
 * @property {string} modelId
 * @property {number} version - Integer
 * @property {TwinProperties} properties - The desired & reported properties
 * @property {TwinTags} tags
 */

export const Types = {}