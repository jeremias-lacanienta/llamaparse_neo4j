// Neo4j Cypher Import Script
// Generated on 2025-05-01 21:24:02
// This script will create a graph representation of the contract

BEGIN

// Uncomment to clear existing data before import
// MATCH (n) DETACH DELETE n;

CREATE (c:Contract {title: 'JOINT TECHNOLOGY DEVELOPMENT AND LICENSING AGREEMENT', effectiveDate: '', documentType: 'LABEL_0' });
CREATE (p0:Party {name: 'OmniSynapse Technologies, Inc.', type: 'Corporation' });
CREATE (p0)-[:PARTY_TO]->(c);
CREATE (s0_0:Person {name: 'Cynthia D. Travers', title: 'CEO
NeuroCore International B.V.
By' });
CREATE (s0_0)-[:REPRESENTS]->(p0);
CREATE (s0_1:Person {name: 'Cynthia D. Travers', title: 'CEO
NeuroCore International B.V.
By' });
CREATE (s0_1)-[:REPRESENTS]->(p0);
CREATE (p1:Party {name: 'NeuroCore International B.V.', type: 'Dutch Private Limited Company' });
CREATE (p1)-[:PARTY_TO]->(c);
CREATE (p2:Party {name: 'Intellectual Property', type: 'Organization' });
CREATE (p2)-[:PARTY_TO]->(c);
CREATE (p3:Party {name: 'Joint Steering Committee', type: 'Organization' });
CREATE (p3)-[:PARTY_TO]->(c);
CREATE (p4:Party {name: 'ISO 13485', type: 'Organization' });
CREATE (p4)-[:PARTY_TO]->(c);
CREATE (p5:Party {name: 'CE Mark', type: 'Organization' });
CREATE (p5)-[:PARTY_TO]->(c);
CREATE (p6:Party {name: 'Each Party', type: 'Organization' });
CREATE (p6)-[:PARTY_TO]->(c);
CREATE (a0:Article {number: 'I', title: 'DEFINITIONS' });
CREATE (c)-[:CONTAINS]->(a0);
CREATE (s0_0:Section {number: '1.1', title: '"Affiliate" shall mean any entity directly or indirectly controlling, controlled by, or under common control with a Party.', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_0);
CREATE (s0_1:Section {number: '1.2', title: '"Background IP" shall mean any Intellectual Property owned or controlled by a Party prior to or independent of the', content: 'Effective Date.
1.3  "Foreground IP" shall mean   any Intellectual Property developed  jointly or individually in the course of this
Agreement.
1.4  "Field of Use" shall mean   exclusively neural-responsive biofeedback  technology  for cognitive rehabilitation
applications.
1.5 "Net Revenue" shall mean gross income derived from commercial exploitation, less reasonable, documented
expenses incurred.
ARTICLE II -' });
CREATE (a0)-[:HAS_SECTION]->(s0_1);
CREATE (s0_2:Section {number: '1.3', title: '"Foreground IP" shall mean   any Intellectual Property developed  jointly or individually in the course of this', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_2);
CREATE (s0_3:Section {number: '1.4', title: '"Field of Use" shall mean   exclusively neural-responsive biofeedback  technology  for cognitive rehabilitation', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_3);
CREATE (s0_4:Section {number: '1.5', title: '"Net Revenue" shall mean gross income derived from commercial exploitation, less reasonable, documented', content: 'expenses incurred.
ARTICLE II -' });
CREATE (a0)-[:HAS_SECTION]->(s0_4);
CREATE (s0_5:Section {number: 'y', title: '1.2 "Background IP" shall mean any Intellectual Property owned or controlled by a Party prior to or independent of the', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_5);
CREATE (s0_6:Section {number: 'e', title: '1.3  "Foreground IP" shall mean   any Intellectual Property developed  jointly or individually in the course of this', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_6);
CREATE (s0_7:Section {number: 't', title: '1.4  "Field of Use" shall mean   exclusively neural-responsive biofeedback  technology  for cognitive rehabilitation', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_7);
CREATE (s0_8:Section {number: 's', title: '1.5 "Net Revenue" shall mean gross income derived from commercial exploitation, less reasonable, documented', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_8);
CREATE (s0_9:Section {number: 'd', title: 'ARTICLE II -', content: '' });
CREATE (a0)-[:HAS_SECTION]->(s0_9);
CREATE (a1:Article {number: 'II', title: 'PURPOSE AND SCOPE' });
CREATE (c)-[:CONTAINS]->(a1);
CREATE (s1_0:Section {number: '2.1', title: 'The Parties agree to collaborate on the design, development, and global commercialization of a joint technology', content: 'platform ("Joint Platform") for the Field of Use.' });
CREATE (a1)-[:HAS_SECTION]->(s1_0);
CREATE (s1_1:Section {number: '2.2', title: 'The scope includes co-development of software algorithms, hardware integration, and AI model training datasets', content: 'sourced from anonymized clinical trials.
ARTICLE III -' });
CREATE (a1)-[:HAS_SECTION]->(s1_1);
CREATE (s1_2:Section {number: 'e', title: '2.2 The scope includes co-development of software algorithms, hardware integration, and AI model training datasets', content: '' });
CREATE (a1)-[:HAS_SECTION]->(s1_2);
CREATE (s1_3:Section {number: 's', title: 'ARTICLE III -', content: '' });
CREATE (a1)-[:HAS_SECTION]->(s1_3);
CREATE (a2:Article {number: 'III', title: 'GOVERNANCE STRUCTURE' });
CREATE (c)-[:CONTAINS]->(a2);
CREATE (s2_0:Section {number: '3.1', title: 'Joint Steering Committee (JSC)', content: '- Comprised of 3 representatives from each Party.
- Meets quarterly (or ad hoc) to review milestones and budget allocations.
- Decisions shall be made by supermajority (i.e., 4 of 6 votes).' });
CREATE (a2)-[:HAS_SECTION]->(s2_0);
CREATE (s2_1:Section {number: '3.2', title: 'Deadlock Resolution', content: '- If the JSC reaches an impasse exceeding 30 days, the matter shall be escalated to the respective CEOs.
- If unresolved within 60 days, mediation in The Hague under ICC rules shall be mandatory before arbitration.
ARTICLE IV -' });
CREATE (a2)-[:HAS_SECTION]->(s2_1);
CREATE (s2_2:Section {number: 'y', title: '- Meets quarterly (or ad hoc) to review milestones and budget allocations.', content: '' });
CREATE (a2)-[:HAS_SECTION]->(s2_2);
CREATE (s2_3:Section {number: 's', title: '- If unresolved within 60 days, mediation in The Hague under ICC rules shall be mandatory before arbitration.', content: '' });
CREATE (a2)-[:HAS_SECTION]->(s2_3);
CREATE (a3:Article {number: 'IV', title: 'INTELLECTUAL PROPERTY' });
CREATE (c)-[:CONTAINS]->(a3);
CREATE (s3_0:Section {number: '4.1', title: 'Ownership', content: '- Background IP remains with the contributing Party.
- Foreground IP created solely by one Party shall be owned by that Party, but licensed to the other under Clause 4.3.
- Jointly developed Foreground IP shall be co-owned on a 50/50 basis.' });
CREATE (a3)-[:HAS_SECTION]->(s3_0);
CREATE (s3_1:Section {number: '4.2', title: 'Prosecution and Maintenance', content: '- Each Party is responsible for prosecuting and maintaining its own IP.
- Joint IP shall be prosecuted by NeuroCore, with costs shared pro rata.' });
CREATE (a3)-[:HAS_SECTION]->(s3_1);
CREATE (s3_2:Section {number: '4.3', title: 'Licensing', content: '- OmniSynapse grants NeuroCore a perpetual, royalty-free, sublicensable license to its Background IP strictly within the
Field of Use.
- NeuroCore grants OmniSynapse a non-exclusive, royalty-bearing license to deploy clinical datasets worldwide outside
of the Field of Use.
ARTICLE V -' });
CREATE (a3)-[:HAS_SECTION]->(s3_2);
CREATE (s3_3:Section {number: 'y', title: '- Foreground IP created solely by one Party shall be owned by that Party, but licensed to the other under Clause 4.3.', content: '' });
CREATE (a3)-[:HAS_SECTION]->(s3_3);
CREATE (s3_4:Section {number: 's', title: '4.2 Prosecution and Maintenance', content: '' });
CREATE (a3)-[:HAS_SECTION]->(s3_4);
CREATE (s3_5:Section {number: 'P', title: '- Joint IP shall be prosecuted by NeuroCore, with costs shared pro rata.', content: '' });
CREATE (a3)-[:HAS_SECTION]->(s3_5);
CREATE (s3_6:Section {number: 'e', title: '- NeuroCore grants OmniSynapse a non-exclusive, royalty-bearing license to deploy clinical datasets worldwide outside', content: '' });
CREATE (a3)-[:HAS_SECTION]->(s3_6);
CREATE (s3_7:Section {number: 'e', title: 'ARTICLE V -', content: '' });
CREATE (a3)-[:HAS_SECTION]->(s3_7);
CREATE (a4:Article {number: 'V', title: 'COMMERCIAL TERMS' });
CREATE (c)-[:CONTAINS]->(a4);
CREATE (s4_0:Section {number: '5.1', title: 'Revenue Sharing', content: '- Net Revenues shall be split 60% (NeuroCore) / 40% (OmniSynapse), subject to annual audit and reconciliation.' });
CREATE (a4)-[:HAS_SECTION]->(s4_0);
CREATE (s4_1:Section {number: '5.2', title: 'Milestone Payments', content: '- $2,500,000 upon achievement of ISO 13485 certification.
- $5,000,000 upon CE Mark approval of the Joint Platform.' });
CREATE (a4)-[:HAS_SECTION]->(s4_1);
CREATE (s4_2:Section {number: '5.3', title: 'Audit Rights', content: '- Either Party may audit the other\'s records once per year upon 30 days\' notice, at its own cost. Discrepancies
exceeding 5% shall trigger full reimbursement plus 10% interest.
ARTICLE VI -' });
CREATE (a4)-[:HAS_SECTION]->(s4_2);
CREATE (s4_3:Section {number: 'n', title: '5.2 Milestone Payments', content: '' });
CREATE (a4)-[:HAS_SECTION]->(s4_3);
CREATE (s4_4:Section {number: 'n', title: '- $5,000,000 upon CE Mark approval of the Joint Platform.', content: '' });
CREATE (a4)-[:HAS_SECTION]->(s4_4);
CREATE (s4_5:Section {number: 't', title: 'Discrepancies', content: '' });
CREATE (a4)-[:HAS_SECTION]->(s4_5);
CREATE (s4_6:Section {number: 't', title: 'ARTICLE VI -', content: '' });
CREATE (a4)-[:HAS_SECTION]->(s4_6);
CREATE (a5:Article {number: 'VI', title: 'TERM AND TERMINATION' });
CREATE (c)-[:CONTAINS]->(a5);
CREATE (s5_0:Section {number: '6.1', title: 'Term', content: '- Initial term: 10 years from Effective Date. Automatically renewable unless terminated under this Article.' });
CREATE (a5)-[:HAS_SECTION]->(s5_0);
CREATE (s5_1:Section {number: '6.2', title: 'Termination for Cause', content: '- If a material breach is not cured within 90 days of notice, the non-breaching Party may terminate this Agreement.' });
CREATE (a5)-[:HAS_SECTION]->(s5_1);
CREATE (s5_2:Section {number: '6.3', title: 'Effects of Termination', content: '- License  rights granted  prior to termination remain   in effect for 5 years  post-termination, subject  to continued
compliance.
- All Foreground IP jointly developed remains co-owned and exploitable by either Party.
ARTICLE VII -' });
CREATE (a5)-[:HAS_SECTION]->(s5_2);
CREATE (s5_3:Section {number: 'e', title: 'Automatically renewable unless terminated under this Article.', content: '' });
CREATE (a5)-[:HAS_SECTION]->(s5_3);
CREATE (s5_4:Section {number: 't', title: '6.3 Effects of Termination', content: '' });
CREATE (a5)-[:HAS_SECTION]->(s5_4);
CREATE (s5_5:Section {number: 'e', title: '- All Foreground IP jointly developed remains co-owned and exploitable by either Party.', content: '' });
CREATE (a5)-[:HAS_SECTION]->(s5_5);
CREATE (a6:Article {number: 'VII', title: 'REPRESENTATIONS AND WARRANTIES' });
CREATE (c)-[:CONTAINS]->(a6);
CREATE (s6_0:Section {number: '7.1', title: 'Each Party represents that it:', content: '- Has full authority to enter into this Agreement.
- Is not bound by conflicting obligations.
- Will not knowingly infringe on third-party IP.
ARTICLE VIII -' });
CREATE (a6)-[:HAS_SECTION]->(s6_0);
CREATE (s6_1:Section {number: 't', title: '- Is not bound by conflicting obligations.', content: '' });
CREATE (a6)-[:HAS_SECTION]->(s6_1);
CREATE (s6_2:Section {number: 'P', title: 'ARTICLE VIII -', content: '' });
CREATE (a6)-[:HAS_SECTION]->(s6_2);
CREATE (a7:Article {number: 'VIII', title: 'INDEMNIFICATION AND LIMITATION OF LIABILITY' });
CREATE (c)-[:CONTAINS]->(a7);
CREATE (s7_0:Section {number: '8.1', title: 'Indemnification', content: '- Each Party shall indemnify the other from any third-party claim arising from its breach, negligence, or willful
misconduct.' });
CREATE (a7)-[:HAS_SECTION]->(s7_0);
CREATE (s7_1:Section {number: '8.2', title: 'Limitation of Liability', content: '- Liability is capped at $10,000,000, except for breaches of confidentiality, IP infringement, or indemnity obligations.
ARTICLE IX -' });
CREATE (a7)-[:HAS_SECTION]->(s7_1);
CREATE (s7_2:Section {number: 't', title: '8.2 Limitation of Liability', content: '' });
CREATE (a7)-[:HAS_SECTION]->(s7_2);
CREATE (s7_3:Section {number: 's', title: 'ARTICLE IX -', content: '' });
CREATE (a7)-[:HAS_SECTION]->(s7_3);
CREATE (a8:Article {number: 'IX', title: 'CONFIDENTIALITY' });
CREATE (c)-[:CONTAINS]->(a8);
CREATE (s8_0:Section {number: '9.1', title: 'All information marked "Confidential" or reasonably understood to be proprietary shall be protected for 10 years after', content: 'termination.' });
CREATE (a8)-[:HAS_SECTION]->(s8_0);
CREATE (s8_1:Section {number: '9.2', title: 'Disclosure is permitted only to Affiliates, subcontractors, and legal advisors bound by similar obligations.', content: 'ARTICLE X -' });
CREATE (a8)-[:HAS_SECTION]->(s8_1);
CREATE (s8_2:Section {number: 'n', title: '9.2 Disclosure is permitted only to Affiliates, subcontractors, and legal advisors bound by similar obligations.', content: '' });
CREATE (a8)-[:HAS_SECTION]->(s8_2);
CREATE (a9:Article {number: 'X', title: 'MISCELLANEOUS' });
CREATE (c)-[:CONTAINS]->(a9);
CREATE (s9_0:Section {number: '10.1', title: 'Force Majeure - No Party shall be liable for delays due to acts beyond reasonable control.', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_0);
CREATE (s9_1:Section {number: '10.2', title: 'Assignment - May not be assigned without prior written consent, except to an Affiliate or in merger/acquisition.', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_1);
CREATE (s9_2:Section {number: '10.3', title: 'Entire Agreement - This document and its Exhibits constitute the entire agreement.', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_2);
CREATE (s9_3:Section {number: '10.4', title: 'Governing Law - Laws of the Netherlands shall govern, excluding conflict of laws principles.', content: 'EXHIBITS
- Exhibit A: Joint Platform Technical Specifications
- Exhibit B: Development Milestones and Timelines
- Exhibit C: IP Ownership Matrix and Contribution Ledger
- Exhibit D: Dispute Escalation Flowchart
- Exhibit E: Confidential Information Handling Protocol
IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.
OmniSynapse Technologies, Inc.
By: _______________________
Name: Cynthia D. Travers
Title: CEO
NeuroCore International B.V.
By: _______________...' });
CREATE (a9)-[:HAS_SECTION]->(s9_3);
CREATE (s9_4:Section {number: 'l', title: '10.2 Assignment - May not be assigned without prior written consent, except to an Affiliate or in merger/acquisition.', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_4);
CREATE (s9_5:Section {number: 't', title: '10.4 Governing Law - Laws of the Netherlands shall govern, excluding conflict of laws principles.', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_5);
CREATE (s9_6:Section {number: 'e', title: 'OmniSynapse Technologies, Inc.', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_6);
CREATE (s9_7:Section {number: 'D', title: 'Travers', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_7);
CREATE (s9_8:Section {number: 'V', title: 'By: _______________________', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_8);
CREATE (s9_9:Section {number: 'r', title: 'Lars van Beek', content: '' });
CREATE (a9)-[:HAS_SECTION]->(s9_9);
CREATE (a10:Article {number: 'JOINT TECHNOLOGY DEVELOPMENT AND LICENSING AGREEMENT
Between', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a10);
CREATE (s10_0:Section {number: '10.1', title: 'Force Majeure - No Party shall be liable for delays due to acts beyond reasonable control.', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_0);
CREATE (s10_1:Section {number: '10.2', title: 'Assignment - May not be assigned without prior written consent, except to an Affiliate or in merger/acquisition.', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_1);
CREATE (s10_2:Section {number: '10.3', title: 'Entire Agreement - This document and its Exhibits constitute the entire agreement.', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_2);
CREATE (s10_3:Section {number: '10.4', title: 'Governing Law - Laws of the Netherlands shall govern, excluding conflict of laws principles.', content: 'EXHIBITS
- Exhibit A: Joint Platform Technical Specifications
- Exhibit B: Development Milestones and Timelines
- Exhibit C: IP Ownership Matrix and Contribution Ledger
- Exhibit D: Dispute Escalation Flowchart
- Exhibit E: Confidential Information Handling Protocol
IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.
OmniSynapse Technologies, Inc.
By: _______________________
Name: Cynthia D. Travers
Title: CEO
NeuroCore International B.V.
By: _______________...' });
CREATE (a10)-[:HAS_SECTION]->(s10_3);
CREATE (s10_4:Section {number: 'l', title: '10.2 Assignment - May not be assigned without prior written consent, except to an Affiliate or in merger/acquisition.', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_4);
CREATE (s10_5:Section {number: 't', title: '10.4 Governing Law - Laws of the Netherlands shall govern, excluding conflict of laws principles.', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_5);
CREATE (s10_6:Section {number: 'e', title: 'OmniSynapse Technologies, Inc.', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_6);
CREATE (s10_7:Section {number: 'D', title: 'Travers', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_7);
CREATE (s10_8:Section {number: 'V', title: 'By: _______________________', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_8);
CREATE (s10_9:Section {number: 'r', title: 'Lars van Beek', content: '' });
CREATE (a10)-[:HAS_SECTION]->(s10_9);
CREATE (a11:Article {number: 'DEFINITIONS', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a11);
CREATE (a12:Article {number: 'Intellectual Property owned or controlled by a Party prior to or independent of the', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a12);
CREATE (a13:Article {number: 'Intellectual Property developed  jointly or individually in the course of this', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a13);
CREATE (a14:Article {number: 'PURPOSE AND SCOPE', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a14);
CREATE (a15:Article {number: 'AI model training datasets', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a15);
CREATE (a16:Article {number: 'GOVERNANCE STRUCTURE', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a16);
CREATE (a17:Article {number: 'Deadlock Resolution', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a17);
CREATE (a18:Article {number: 'INTELLECTUAL PROPERTY', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a18);
CREATE (a19:Article {number: 'Ownership', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a19);
CREATE (a20:Article {number: 'Prosecution and Maintenance', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a20);
CREATE (a21:Article {number: 'Licensing', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a21);
CREATE (a22:Article {number: 'Background IP strictly within the', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a22);
CREATE (a23:Article {number: 'COMMERCIAL TERMS', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a23);
CREATE (a24:Article {number: 'Revenue Sharing', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a24);
CREATE (a25:Article {number: 'Milestone Payments', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a25);
CREATE (a26:Article {number: 'Audit Rights', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a26);
CREATE (a27:Article {number: 'Discrepancies', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a27);
CREATE (a28:Article {number: 'TERM AND TERMINATION', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a28);
CREATE (a29:Article {number: 'Term', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a29);
CREATE (a30:Article {number: 'Termination for Cause', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a30);
CREATE (a31:Article {number: 'Effects of Termination', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a31);
CREATE (a32:Article {number: 'REPRESENTATIONS AND WARRANTIES', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a32);
CREATE (a33:Article {number: 'INDEMNIFICATION AND LIMITATION OF LIABILITY', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a33);
CREATE (a34:Article {number: 'Indemnification', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a34);
CREATE (a35:Article {number: 'Limitation of Liability', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a35);
CREATE (a36:Article {number: 'CONFIDENTIALITY', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a36);
CREATE (a37:Article {number: 'MISCELLANEOUS', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a37);
CREATE (a38:Article {number: 'EXHIBITS', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a38);
CREATE (a39:Article {number: 'Joint Platform Technical Specifications', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a39);
CREATE (a40:Article {number: 'Development Milestones and Timelines', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a40);
CREATE (a41:Article {number: 'IP Ownership Matrix and Contribution Ledger', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a41);
CREATE (a42:Article {number: 'Dispute Escalation Flowchart', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a42);
CREATE (a43:Article {number: 'Confidential Information Handling Protocol', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a43);
CREATE (a44:Article {number: 'Travers', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a44);
CREATE (a45:Article {number: 'CEO', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a45);
CREATE (a46:Article {number: 'Lars van Beek', title: 'UNTITLED' });
CREATE (c)-[:CONTAINS]->(a46);

COMMIT
