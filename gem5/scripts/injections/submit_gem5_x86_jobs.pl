#!/usr/bin/perl -w

my $SPARE = 0;
my $USERNAME = $ENV{LOGNAME};
my $APPROX_DIR = $ENV{APPROXGEM5};

open my $file, '<', "max_jobs.txt";
my $MAX_JOBS = <$file>;
close $file;
#my $MAX_JOBS = $firstline;
#my $MAX_JOBS=120;
print "Max Jobs = $MAX_JOBS\n";


$num_args = $#ARGV+1;
if($num_args != 5) {
	print "Usage: ./submit_gem5_jobs.pl <gem5_inj_list> <app_name> <app_ckpt_num> <app_output(in m5out)> <disk image(in dist/m5/system/disks)>\n";
	die;
}
my $app_name = $ARGV[1];
my $ckpt = $ARGV[2];
my $app_output = $ARGV[3];
my $disk_image = $ARGV[4];
print "App name: $app_name\n";
open(JOB_LIST, "<$ARGV[0]");
$go_to_sleep = 1;

$job_list_length = `wc -l $ARGV[0]`;
if ($job_list_length =~/^(\d+)/ ) {
    $num_jobs = $1;
}
print "Total number of jobs: $num_jobs\n";

my $job_sub_file = "$APPROX_DIR/fault_list_output/condor_scripts/all_jobs_$num_jobs.condor";

if($num_jobs == 0) {
	exit(1);
}

my $num_submitted_jobs = 0;

while ($go_to_sleep == 1) {

	my $empty_slots = 0;
	
	# busy_nodes = # jobs that are running
	# total_nodes = # nodes that are available
	# empty_slots = # nodes that are unclaimed and idle
	# my_nodes = # of my jobs that are running.
	

    # dynamically update number of condor jobs from file
    open my $file, '<', "max_jobs.txt";
    $MAX_JOBS = <$file>;
    close $file;


    # num jobs on condor, not running
    my $num_running_jobs = `condor_q $USERNAME | tail -1 | cut -d' ' -f1`;
	$num_running_jobs = int($num_running_jobs);

	if ($num_running_jobs < $MAX_JOBS) {
    	$empty_slots = $MAX_JOBS-$num_running_jobs;
	} else {
		$empty_slots = 0;
	}


	if (($empty_slots>0) && (!eof(JOB_LIST))) {

		open(CONDOR_FILE, ">$job_sub_file");

		print CONDOR_FILE "universe            = vanilla\n";
		print CONDOR_FILE "requirements        = ((target.memory * 2048) >= ImageSize) && ((Arch == \"X86_64\") || (Arch == \"INTEL\"))\n";
		print CONDOR_FILE "Executable          = /bin/sh\n"; 
		print CONDOR_FILE "getenv              = true\n";
		print CONDOR_FILE "notification = error\n\n";

		my $i = 0;
		for ($i=0; $i<$empty_slots; $i++) {

			my $num_per_job = 1; 
			my $job_args = "";
			while (<JOB_LIST>) { 
				my($line) = $_;
				chomp($line);
				#$line=~ s/\s+//g;
				if($line eq "") {
					#print "Found an empty line\n";
					next;
				}


				$num_submitted_jobs++;
				$num_per_job--;

				$job_args = "$APPROX_DIR/gem5/scripts/injections/run_injection_x86_veena.sh $app_name $line $ckpt $app_output $disk_image $num_submitted_jobs";

				if($num_per_job <= 0) {
					last; 
				}
			}
			if($job_args ne "") { 
				print CONDOR_FILE "arguments       = $job_args\n" ;
				print CONDOR_FILE "periodic_remove = (RemoteWallClockTime > 100*10*60)\n" ;
				print CONDOR_FILE "output          = /dev/null\n" ;
				print CONDOR_FILE "error           = /dev/null\n" ;
				print CONDOR_FILE "queue\n\n" ;

				#@words = split(/\//,$line);
				#print CONDOR_FILE "output          = condor_output/$words[2].output\n" ;
				#print CONDOR_FILE "error           = condor_output/$words[2].err\n" ;
				#print CONDOR_FILE "periodic_remove = (RemoteWallClockTime > 10*10*60*60)\n" ;
				# remove if mem exceeds 2 gig
				#print CONDOR_FILE "periodic_remove = (ImageSize > 2*1024*1024)\n" ;
			}

			if($num_per_job > 0) { # no more jobs to submit
				$go_to_sleep = 0;
				last;
			}
		}

		close(CONDOR_FILE);

		system "condor_submit $job_sub_file";

		printf "Progress : %.2f percent, Number of Submitted jobs : %d\n", ($num_submitted_jobs*100.0/$num_jobs, $num_submitted_jobs);

	}
	if ($go_to_sleep) {
		#$st = 10 + rand() * 100; # sleep time
		$st = 8;

		sleep ($st);
	}
}

close(JOB_LIST);


