// Neo4j Cypher Import Script
// Generated on 2025-05-15 16:55:26
// This script will create a graph representation of the contract

BEGIN

// Uncomment to clear existing data before import
// MATCH (n) DETACH DELETE n;

CREATE (c:Contract {title: 'JOINT TECHNOLOGY DEVELOPMENT AND LICENSING AGREEMENT', effectiveDate: 'April 29, 2025', documentType: 'Agreement', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced', importTimestamp: '2025-05-15 16:55:26' });
CREATE (a0:Article {number: 'Unknown
JOINT TECHNOLOGY DEVELOPMENT AND LICENSING AGREEMENT
Between', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a0);
CREATE (s0_0:Section {number: 'c', title: '(a Delaware Corporation)', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a0)-[:HAS_SECTION]->(s0_0);
CREATE (a1:Article {number: 'and', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a1);
CREATE (s1_0:Section {number: 'V', title: '(a Netherlands Besloten Vennootschap)', content: 'Effective Date: April 29, 2025', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a1)-[:HAS_SECTION]->(s1_0);
CREATE (a2:Article {number: 'I', title: 'DEFINITIONS', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a2);
CREATE (a3:Article {number: 'DEFINITIONS', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a3);
CREATE (s3_0:Section {number: '1.1', title: '"Affiliate" shall mean any entity directly or indirectly controlling, controlled by, or under common control with a Party.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a3)-[:HAS_SECTION]->(s3_0);
CREATE (s3_1:Section {number: 'y', title: '1.2 "Background IP"', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a3)-[:HAS_SECTION]->(s3_1);
CREATE (s3_2:Section {number: '1.2', title: '"Background IP"', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a3)-[:HAS_SECTION]->(s3_2);
CREATE (a4:Article {number: 'shall mean any Intellectual Property owned or controlled by a Party prior to or independent of the', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a4);
CREATE (s4_0:Section {number: 'e', title: '1.3  "Foreground IP"', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a4)-[:HAS_SECTION]->(s4_0);
CREATE (s4_1:Section {number: '1.3', title: '"Foreground IP"', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a4)-[:HAS_SECTION]->(s4_1);
CREATE (a5:Article {number: 'shall mean   any Intellectual Property developed  jointly or individually in the course of this', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a5);
CREATE (s5_0:Section {number: 't', title: '1.4  "Field of Use" shall mean   exclusively neural-', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a5)-[:HAS_SECTION]->(s5_0);
CREATE (s5_1:Section {number: '1.4', title: '"Field of Use" shall mean   exclusively neural-', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a5)-[:HAS_SECTION]->(s5_1);
CREATE (a6:Article {number: 'responsive biofeedback  technology  for cognitive rehabilitation', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a6);
CREATE (s6_0:Section {number: 's', title: '1.5 "Net Revenue" shall mean gross income derived from commercial exploitation, less reasonable,', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a6)-[:HAS_SECTION]->(s6_0);
CREATE (s6_1:Section {number: '1.5', title: '"Net Revenue" shall mean gross income derived from commercial exploitation, less reasonable,', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a6)-[:HAS_SECTION]->(s6_1);
CREATE (a7:Article {number: 'documented', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a7);
CREATE (a8:Article {number: 'II', title: 'PURPOSE AND SCOPE', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a8);
CREATE (a9:Article {number: 'PURPOSE AND SCOPE', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a9);
CREATE (s9_0:Section {number: '2.1', title: 'The Parties agree to collaborate on the design, development,', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a9)-[:HAS_SECTION]->(s9_0);
CREATE (a10:Article {number: 'and global commercialization of a joint technology', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a10);
CREATE (s10_0:Section {number: 'e', title: '2.2 The scope includes co-development of software algorithms, hardware integration,', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a10)-[:HAS_SECTION]->(s10_0);
CREATE (s10_1:Section {number: '2.2', title: 'The scope includes co-development of software algorithms, hardware integration,', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a10)-[:HAS_SECTION]->(s10_1);
CREATE (a11:Article {number: 'and AI model training datasets', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a11);
CREATE (s11_0:Section {number: 's', title: '---', content: 'File:', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a11)-[:HAS_SECTION]->(s11_0);
CREATE (a12:Article {number: 'Unknown', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a12);
CREATE (a13:Article {number: 'III', title: 'GOVERNANCE STRUCTURE', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a13);
CREATE (a14:Article {number: 'GOVERNANCE STRUCTURE', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a14);
CREATE (s14_0:Section {number: '3.1', title: 'Joint Steering Committee (JSC)', content: '- Comprised of 3 representatives from each Part', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a14)-[:HAS_SECTION]->(s14_0);
CREATE (s14_1:Section {number: 'y', title: '- Meets quarterly (or ad hoc) to review milestones and budget allocations.', content: '- Decisions shall be made by supermajority (i.e., 4 of 6 votes).
3.2', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a14)-[:HAS_SECTION]->(s14_1);
CREATE (a15:Article {number: 'Deadlock Resolution', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a15);
CREATE (s15_0:Section {number: 's', title: '- If unresolved within 60 days, mediation in The Hague under ICC rules shall be mandatory before arbitration.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a15)-[:HAS_SECTION]->(s15_0);
CREATE (a16:Article {number: 'IV', title: 'INTELLECTUAL PROPERTY', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a16);
CREATE (a17:Article {number: 'INTELLECTUAL PROPERTY', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a17);
CREATE (a18:Article {number: 'Ownership', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a18);
CREATE (s18_0:Section {number: 'y', title: '- Foreground IP created solely by one Party shall be owned by that Party, but licensed to the other under Clause 4.3.', content: '- Jointly developed Foreground IP shall be co-owned on a 50/50 basi', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a18)-[:HAS_SECTION]->(s18_0);
CREATE (s18_1:Section {number: 's', title: '4.2', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a18)-[:HAS_SECTION]->(s18_1);
CREATE (a19:Article {number: 'Prosecution and Maintenance', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a19);
CREATE (s19_0:Section {number: 'P', title: '- Joint IP shall be prosecuted by NeuroCore, with costs shared pro rata.', content: '4.3', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a19)-[:HAS_SECTION]->(s19_0);
CREATE (a20:Article {number: 'Licensing', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a20);
CREATE (a21:Article {number: 'sublicensable license to its Background IP strictly within the', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a21);
CREATE (s21_0:Section {number: 'e', title: '- NeuroCore grants OmniSynapse a non-exclusive, royalty-', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a21)-[:HAS_SECTION]->(s21_0);
CREATE (a22:Article {number: 'bearing license to deploy clinical datasets worldwide outside', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a22);
CREATE (a23:Article {number: 'V', title: 'COMMERCIAL TERMS', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a23);
CREATE (a24:Article {number: 'COMMERCIAL TERMS', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a24);
CREATE (a25:Article {number: 'Revenue Sharing', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a25);
CREATE (s25_0:Section {number: 'n', title: '---', content: 'File:', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a25)-[:HAS_SECTION]->(s25_0);
CREATE (a26:Article {number: 'Unknown', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a26);
CREATE (a27:Article {number: 'Milestone Payments', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a27);
CREATE (s27_0:Section {number: 'n', title: '- $5,000,000 upon CE Mark approval of the Joint Platform.', content: '5.3', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a27)-[:HAS_SECTION]->(s27_0);
CREATE (a28:Article {number: 'Audit Rights', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a28);
CREATE (a29:Article {number: 'Discrepancies', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a29);
CREATE (a30:Article {number: 'VI', title: 'TERM AND TERMINATION', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a30);
CREATE (a31:Article {number: 'TERM AND TERMINATION', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a31);
CREATE (a32:Article {number: 'Term', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a32);
CREATE (s32_0:Section {number: 'e', title: 'Automatically renewable unless terminated under this Article.', content: '6.2', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a32)-[:HAS_SECTION]->(s32_0);
CREATE (a33:Article {number: 'Termination for Cause', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a33);
CREATE (s33_0:Section {number: 't', title: '6.3', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a33)-[:HAS_SECTION]->(s33_0);
CREATE (a34:Article {number: 'Effects of Termination', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a34);
CREATE (a35:Article {number: 'subject  to continued', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a35);
CREATE (s35_0:Section {number: 'e', title: '- All Foreground IP jointly developed remains co-owned and exploitable by either Party.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a35)-[:HAS_SECTION]->(s35_0);
CREATE (a36:Article {number: 'VII', title: 'REPRESENTATIONS AND WARRANTIES', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a36);
CREATE (a37:Article {number: 'REPRESENTATIONS AND WARRANTIES', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a37);
CREATE (s37_0:Section {number: '7.1', title: 'Each Party represents that it:', content: '- Has full authority to enter into this Agreemen', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a37)-[:HAS_SECTION]->(s37_0);
CREATE (s37_1:Section {number: 't', title: '- Is not bound by conflicting obligations.', content: '- Will not knowingly infringe on third-party IP.', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a37)-[:HAS_SECTION]->(s37_1);
CREATE (a38:Article {number: 'VIII', title: 'INDEMNIFICATION AND LIMITATION OF LIABILITY', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a38);
CREATE (a39:Article {number: 'INDEMNIFICATION AND LIMITATION OF LIABILITY', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a39);
CREATE (a40:Article {number: 'Indemnification', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a40);
CREATE (a41:Article {number: 'or willful', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a41);
CREATE (s41_0:Section {number: 't', title: '---', content: 'File:', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a41)-[:HAS_SECTION]->(s41_0);
CREATE (a42:Article {number: 'Unknown', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a42);
CREATE (a43:Article {number: 'Limitation of Liability', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a43);
CREATE (a44:Article {number: 'IX', title: 'CONFIDENTIALITY', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a44);
CREATE (a45:Article {number: 'CONFIDENTIALITY', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a45);
CREATE (s45_0:Section {number: '9.1', title: 'All information marked "Confidential" or reasonably understood to be proprietary shall be protected for 10', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a45)-[:HAS_SECTION]->(s45_0);
CREATE (a46:Article {number: 'years after', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a46);
CREATE (s46_0:Section {number: 'n', title: '9.2 Disclosure is permitted only to Affiliates, subcontractors, and legal advisors bound by similar obligations.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a46)-[:HAS_SECTION]->(s46_0);
CREATE (s46_1:Section {number: '9.2', title: 'Disclosure is permitted only to Affiliates, subcontractors, and legal advisors bound by similar obligations.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a46)-[:HAS_SECTION]->(s46_1);
CREATE (a47:Article {number: 'X', title: 'MISCELLANEOUS', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a47);
CREATE (a48:Article {number: 'MISCELLANEOUS', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a48);
CREATE (s48_0:Section {number: '10.1', title: 'Force Majeure - No Party shall be liable for delays due to acts beyond reasonable control.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a48)-[:HAS_SECTION]->(s48_0);
CREATE (s48_1:Section {number: 'l', title: '10.2 Assignment - May not be assigned without prior written consent, except to an Affiliate or in merger/acquisition.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a48)-[:HAS_SECTION]->(s48_1);
CREATE (s48_2:Section {number: '10.2', title: 'Assignment - May not be assigned without prior written consent, except to an Affiliate or in merger/acquisition.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a48)-[:HAS_SECTION]->(s48_2);
CREATE (s48_3:Section {number: '10.3', title: 'Entire Agreement - This document and its Exhibits constitute the entire agreement.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a48)-[:HAS_SECTION]->(s48_3);
CREATE (s48_4:Section {number: 't', title: '10.4 Governing Law - Laws of the Netherlands shall govern, excluding conflict of laws principles.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a48)-[:HAS_SECTION]->(s48_4);
CREATE (s48_5:Section {number: '10.4', title: 'Governing Law - Laws of the Netherlands shall govern, excluding conflict of laws principles.', content: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a48)-[:HAS_SECTION]->(s48_5);
CREATE (a49:Article {number: 'EXHIBITS', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a49);
CREATE (a50:Article {number: 'Joint Platform Technical Specifications', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a50);
CREATE (a51:Article {number: 'Development Milestones and Timelines', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a51);
CREATE (a52:Article {number: 'IP Ownership Matrix and Contribution Ledger', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a52);
CREATE (a53:Article {number: 'Dispute Escalation Flowchart', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a53);
CREATE (a54:Article {number: 'Confidential Information Handling Protocol', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a54);
CREATE (s54_0:Section {number: 'e', title: 'OmniSynapse Technologies, Inc.', content: 'By: _______________________
Name: Cynthia D.', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a54)-[:HAS_SECTION]->(s54_0);
CREATE (a55:Article {number: 'Travers', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a55);
CREATE (a56:Article {number: 'CEO
', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a56);
CREATE (a57:Article {number: 'Unknown', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a57);
CREATE (s57_0:Section {number: 'V', title: 'By: _______________________', content: 'Name: Dr.', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (a57)-[:HAS_SECTION]->(s57_0);
CREATE (a58:Article {number: 'Lars van Beek', title: 'UNTITLED', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
CREATE (c)-[:CONTAINS]->(a58);
CREATE (kp0:KeyProvision {number: 'II', title: 'PURPOSE AND SCOPE', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp0);
CREATE (kp1:KeyProvision {number: 'IV', title: 'INTELLECTUAL PROPERTY', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp1);
CREATE (kp2:KeyProvision {number: 'V', title: 'COMMERCIAL TERMS', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp2);
CREATE (kp3:KeyProvision {number: 'VI', title: 'TERM AND TERMINATION', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp3);
CREATE (kp4:KeyProvision {number: 'VII', title: 'REPRESENTATIONS AND WARRANTIES', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp4);
CREATE (kp5:KeyProvision {number: 'VIII', title: 'INDEMNIFICATION AND LIMITATION OF LIABILITY', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp5);
CREATE (kp6:KeyProvision {number: 'IX', title: 'CONFIDENTIALITY', summary: '', sourceDocument: 'sample_contract_enhanced.json', documentId: 'sample_contract_enhanced' });
MATCH (c:Contract {documentId: 'sample_contract_enhanced'}) CREATE (c)-[:HAS_KEY_PROVISION]->(kp6);

COMMIT
