use strict;
use warnings;
use utf8;
use JSON::PP qw(decode_json);

binmode STDIN, ':raw';
binmode STDOUT, ':encoding(UTF-8)';
binmode STDERR, ':encoding(UTF-8)';

sub timestamp {
    my ($seconds) = @_;
    return sprintf "%02d:%02d:%02d.000", int($seconds / 3600),
        int($seconds / 60) % 60, $seconds % 60;
}

sub chapters {
    my ($report) = @_;
    die "O relatório precisa conter uma lista de blocos.\n"
        unless ref($report) eq 'HASH' && ref($report->{blocos}) eq 'ARRAY';

    my $offset = 0;
    my @cues;
    for my $block (@{$report->{blocos}}) {
        die "Bloco sem nome ou duração válida.\n"
            unless ref($block) eq 'HASH' && defined($block->{nome})
                && !ref($block->{nome}) && $block->{nome} =~ /\S/
                && defined($block->{segundos}) && !ref($block->{segundos})
                && $block->{segundos} =~ /\A[0-9]+\z/;
        next if $block->{segundos} == 0;
        my $title = $block->{nome};
        $title =~ s/\s+/ /g;
        $title =~ s/&/&amp;/g;
        $title =~ s/</&lt;/g;
        $title =~ s/>/&gt;/g;
        my $end = $offset + $block->{segundos};
        push @cues, timestamp($offset) . ' --> ' . timestamp($end) . "\n$title\n";
        $offset = $end;
    }
    return join("\n", "WEBVTT\n", @cues);
}

my $ok = eval {
    local $/;
    my $input = <STDIN>;
    print chapters(decode_json($input // ''));
    1;
};
unless ($ok) {
    print STDERR "Erro ao gerar capítulos: $@";
    exit 2;
}
