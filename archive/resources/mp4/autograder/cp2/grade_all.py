#!/usr/bin/python
import sys
import subprocess
import operator
import json
from datetime import datetime
from grade_mp4cp2part1 import grade_mp4cp2part1
from grade_mp4cp2part2 import grade_mp4cp2part2


def read_lines(filepath):
    content = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if (len(line) == 0) or (line[0] == '#'):
                continue
            content.append(line)
    return content


def grade_student(svndir, student, solutiondir):
    partners = read_lines("{}/partners.txt".format(svndir))
    ignore = False
    if len(partners) == 0:
        ignore = True
    partner = None
    for name in partners:
        if name != student:
            partner = name
            break
    header = "MP4 Checkpoint 2 Grade Report for {}\n".format(student)
    (message, score, total, message_list) = grade_mp4cp2part1(svndir, solutiondir, student)
    message += "\n"
    (message, score, total) = tuple(map(operator.add, (message, score, total),
                                        grade_mp4cp2part2(svndir, solutiondir + "/cp2_pcap")))
    subheader = "Total:\t{} / {}\n\nDetails:\n".format(score, total)
    return header + subheader + message, score, total, partner, ignore, message_list


def manage_partners(grades):
    for name in grades.keys():
        if name not in grades:
            continue
        student = grades[name]
        score = student["score"]
        ignore = student["ignore"]
        if ignore:
            continue
        partner_name = student["partner"]
        if partner_name not in grades:
            continue
        partner = grades[partner_name]
        partner_score = partner["score"]
        partner_ignore = partner["ignore"]
        if partner_ignore:
            del grades[partner_name]
            continue
        if score > partner_score:
            print "Score conflict: {}: {}; {}: {}".format(name, student["score"], partner_name, partner_score)
            del grades[name]
            continue
        else:
            del partner
    return grades


def main():
    if len(sys.argv) < 5:
        print "usage: python grade_all.py <svn_base_directory> <roster_path> <solution_path> <deadline>\n" \
              "ex) python grade_all.py ~/Desktop/ece422_mp4grade ~/Desktop/students.txt " \
              "~/ \"{2016-04-18 18:10:00}\""
        sys.exit(1)

    svn_basedir = sys.argv[1]
    roster_path = sys.argv[2]
    solutiondir = sys.argv[3]
    deadline = sys.argv[4]

    # svn up
    svnup = ["svn", "update", svn_basedir, "-r", deadline]
    try:
        subprocess.call(svnup)
    except OSError:
        print "failed to svn update"
        sys.exit(1)

    global_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    grade_report = "mp4cp2grades_{}.csv".format(str(global_time))

    grades = dict()
    message_list = None

    with open(roster_path, "r") as r:
        for student in r:
            student = student.rstrip()
            svndir = svn_basedir + "/" + student + "/mp4"
            print "Grading " + student
            student_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            (message, score, total, partner, ignore, message_list) = grade_student(svndir, student, solutiondir)

            # write student report
            student_report = "{}_mp4cp2grades_{}.txt".format(student, str(student_time))
            with open(svndir + "/" + student_report, "w", 0) as s:
                s.write(message)
            print "\tTotal: {} / {}".format(score, total)

            # dict used for later partner scoring
            grades[student] = {"score": score, "partner": partner, "ignore": ignore, "report": student_report}

            try:
                svnadd = ["svn", "add", svndir + "/" + student_report]
                subprocess.call(svnadd)
            except OSError:
                print "\tfailed to svn add student grade report"
                pass

    with open("message_list.json", "w") as fp:
        json.dump(message_list, fp, sort_keys=True, indent=4, separators=(',', ': '))
    # manage partner scores
    grades = manage_partners(grades)

    # write instructor report
    with open(grade_report, "w", 0) as gr:
        for name, value in grades.iteritems():
            gr.write(name + "," + str(value["score"]) + "\n")
            partner_name = value["partner"]
            if partner_name is not None:
                gr.write(partner_name + "," + str(value["score"]) + "\n")
                report = value["report"]
                student_report = svn_basedir + "/" + name + "/mp4/" + report
                partner_report = svn_basedir + "/" + partner_name + "/mp4/" + report
                try:
                    svncp = ["svn", "cp", student_report, partner_report]
                    subprocess.call(svncp)
                except OSError:
                    print "\tfailed to svn cp student grade report"
                    pass
    svnadd = ["svn", "add", grade_report]
    try:
        subprocess.call(svnadd)
    except OSError:
        print "failed to svn add grade report"
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
