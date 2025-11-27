export const mockHosts = [
    { id: 'h1', name: 'bi5050-1.if.test.de', fqdn: 'bi5050-1.if.test.de' },
    { id: 'h2', name: 'bi5050-2.if.test.de', fqdn: 'bi5050-2.if.test.de' },
    { id: 'h3', name: 'cimc-pvoip-03.test.de', fqdn: 'cimc-pvoip-03.test.de' },
    { id: 'h4', name: 'cimc-pvoip-04.test.de', fqdn: 'cimc-pvoip-04.test.de' },
    { id: 'h5', name: 'cimc-pvoip-07.test.de', fqdn: 'cimc-pvoip-07.test.de' },
    { id: 'h6', name: 'cimc-pvoip-08.test.de', fqdn: 'cimc-pvoip-08.test.de' },
    { id: 'h7', name: 'cucm-dev-rev-proxy.test.de', fqdn: 'cucm-dev-rev-proxy.test.de' },
    { id: 'h8', name: 'cucm-rev-proxy.test.de', fqdn: 'cucm-rev-proxy.test.de' },
    { id: 'h9', name: 'cucmdevpub.test.de', fqdn: 'cucmdevpub.test.de' },
    { id: 'h10', name: 'cucmdevsub1.test.de', fqdn: 'cucmdevsub1.test.de' },
    { id: 'h11', name: 'cucmdevsub2.test.de', fqdn: 'cucmdevsub2.test.de' },
    { id: 'h12', name: 'cucmexpc1.test.de', fqdn: 'cucmexpc1.test.de' },
    { id: 'h13', name: 'cucmexpc2.test.de', fqdn: 'cucmexpc2.test.de' },
    { id: 'h14', name: 'cucmexpc3.test.de', fqdn: 'cucmexpc3.test.de' },
    { id: 'h15', name: 'cucmexpc4.test.de', fqdn: 'cucmexpc4.test.de' },
    { id: 'h16', name: 'cucmpub.test.de', fqdn: 'cucmpub.test.de' },
    { id: 'h17', name: 'cucmsub1.test.de', fqdn: 'cucmsub1.test.de' },
    { id: 'h18', name: 'cucmsub2.test.de', fqdn: 'cucmsub2.test.de' },
    { id: 'h19', name: 'cucmtftp1.test.de', fqdn: 'cucmtftp1.test.de' },
    { id: 'h20', name: 'cucmtftp2.test.de', fqdn: 'cucmtftp2.test.de' },
    { id: 'h21', name: 'cucmtrp1.test.de', fqdn: 'cucmtrp1.test.de' },
    { id: 'h22', name: 'cucmtrp2.test.de', fqdn: 'cucmtrp2.test.de' },
    { id: 'h23', name: 'cucmweb1.test.de', fqdn: 'cucmweb1.test.de' },
    { id: 'h24', name: 'cucmweb2.test.de', fqdn: 'cucmweb2.test.de' },
    { id: 'h25', name: 'expe1-publ1.voip.test.de', fqdn: 'expe1-publ1.voip.test.de' },
    { id: 'h26', name: 'expe2-publ2.voip.test.de', fqdn: 'expe2-publ2.voip.test.de' },
    { id: 'h27', name: 'expe3-publ1.voip.test.de', fqdn: 'expe3-publ1.voip.test.de' },
    { id: 'h28', name: 'expe4-publ2.voip.test.de', fqdn: 'expe4-publ2.voip.test.de' },
    { id: 'h29', name: 'gts3-cisco4321-1.if.test.de', fqdn: 'gts3-cisco4321-1.if.test.de' },
    { id: 'h30', name: 'gts3-cisco4321-2.if.test.de', fqdn: 'gts3-cisco4321-2.if.test.de' },
    { id: 'h31', name: 'mind01-cisco4321-1.if.test.de', fqdn: 'mind01-cisco4321-1.if.test.de' },
    { id: 'h32', name: 'mind01-cisco4351-1.if.test.de', fqdn: 'mind01-cisco4351-1.if.test.de' },
];

export const mockNetworks = [
    {
        id: 'n1',
        name: 'Voice-ab-VLAN_TT',
        cidr: '10.71.64.0/20',
        description: 'Voice VLAN Analog-Gateways'
    },
    {
        id: 'n2',
        name: 'Voice-VLAN_TT',
        cidr: '10.71.0.0/18',
        description: 'Voice VLAN'
    },
    {
        id: 'n3',
        name: 'Voice-VLAN_FHC',
        cidr: '10.71.144.0/21',
        description: 'Voice VLAN FH'
    },
];

export const mockGroups = [
    {
        id: 'g1',
        name: 'CallManager',
        members: ['h16', 'h17', 'h18', 'h19', 'h20', 'h23', 'h24', 'h9', 'h10', 'h11'] // cucmpub, cucmsub1, cucmsub2, cucmtftp1, cucmtftp2, cucmweb1, cucmweb2, cucmdevpub, cucmdevsub1, cucmdevsub2
    },
    {
        id: 'g2',
        name: 'Gateway-extern',
        members: ['h29', 'h30', 'h31', 'h32', 'n1'] // gts3-cisco4321-1, gts3-cisco4321-2, mind01-cisco4321-1, mind01-cisco4351-1, Voice-ab-VLAN_TT
    },
    {
        id: 'g3',
        name: 'Phones',
        members: ['n1', 'n2', 'n3'] // Voice-ab-VLAN_TT, Voice-VLAN_TT, Voice-VLAN_FHC
    },
];

