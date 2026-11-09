.class public final Lcom/eip/netsniffer/VersionChecker;
.super Ljava/lang/Object;
.source "VersionChecker.kt"

# NOTE: stand-in for a class that was missing from the shipped dex files.
# The remote update gate is disabled: no forced dialog, no force-close.

# static fields
.field public static final INSTANCE:Lcom/eip/netsniffer/VersionChecker;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/eip/netsniffer/VersionChecker;

    invoke-direct {v0}, Lcom/eip/netsniffer/VersionChecker;-><init>()V

    sput-object v0, Lcom/eip/netsniffer/VersionChecker;->INSTANCE:Lcom/eip/netsniffer/VersionChecker;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public final check(Landroid/app/Activity;)V
    .locals 0

    return-void
.end method
