for (var i=0; i < 6; i++)
{
    Math.max(i);
}

//negative zero
function foo(a,b)
{
    var c = Math.max(a,b);
    return 1/c;
}
print(foo(-0,0));
print(foo(-0,0));
result = foo(0,-0);
if (result === -Infinity) {
    throw Error("-Infinity found!");
}

