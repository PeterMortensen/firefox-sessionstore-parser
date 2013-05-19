#! /bin/sh

testname="$0.d"
rm -rf "$testname"
mkdir "$testname"
cd "$testname"

sessionstoreparser ../sessionstore.js_closedwindows > output
echo $? > exitstatus

cat << EOF > expectedoutput
http://url2/
EOF
echo 0 > expectedexitstatus

diff -u output expectedoutput &&
diff -u exitstatus expectedexitstatus
