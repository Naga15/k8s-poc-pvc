const fs = require('fs');
const execSync = require('child_process').execSync;

// Load clusterroles
const clusterRoles = JSON.parse(execSync('kubectl get clusterroles -o json').toString()).items;

// Filter for clusterroles with cluster-admin permissions
const clusterAdminRoles = clusterRoles.filter(cr => cr.rules.some(rule => rule.apiGroups.includes("") && rule.resources.includes("*") && rule.verbs.includes("*")));

// Load clusterrolebindings
const clusterRoleBindings = JSON.parse(execSync('kubectl get clusterrolebindings -o json').toString()).items;

// Filter for clusterrolebindings with cluster-admin roles
const clusterAdminRoleBindings = clusterRoleBindings.filter(crb => crb.roleRef.kind === 'ClusterRole' && clusterAdminRoles.some(role => role.metadata.name === crb.roleRef.name));

// Filter for non-namespace-scoped users and service accounts
const clusterAdminSubjects = clusterAdminRoleBindings
  .filter(crb => crb.subjects)
  .map(crb => crb.subjects.filter(subj => !subj.namespace))
  .flat()
  .filter(subj => !['ServiceAccount', 'Group'].includes(subj.kind));

// Format data as an array of objects
const data = clusterAdminSubjects.map(subj => ({
  name: subj.name,
  kind: subj.kind,
  clusterRoles: clusterAdminRoleBindings.filter(crb => crb.subjects.some(s => s.name === subj.name && s.kind === subj.kind)).map(crb => crb.roleRef.name),
}));

// Write to CSV file
const csv = data.reduce((acc, curr) => acc + `${curr.name},${curr.kind},${curr.clusterRoles.join('|')}\n`, 'Name,Kind,Cluster Roles\n');
fs.writeFileSync('cluster-admin-subjects.csv', csv);

console.log(`Wrote ${data.length} subjects to cluster-admin-subjects.csv`);
